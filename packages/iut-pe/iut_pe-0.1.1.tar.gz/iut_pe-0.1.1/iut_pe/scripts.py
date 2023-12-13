#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

from iut_pe.scodoc import ScodocAPI
from iut_pe.helpers import civilite, pdf_name, FileHandler, default_parser, load_config
import yaml
import json
import os
import argparse
from pathlib import Path
import subprocess


def ping():
    """ Fiche poursuite d'études ScoDoc
        iut-pe-ping: permet de tester la connection avec l'API de ScoDoc.
    """
    # args parser
    parser = default_parser("iut-pe-ping", ping.__doc__)
    args = parser.parse_args()
    config = load_config(args.config)
    api = ScodocAPI(**config["scodoc"])
    api.ping()


def fetch():
    """ Récupère les informations étudiants depuis ScoDoc et les enregistre dans une base de donnée locale.
    """
    # args parser
    parser = default_parser("iut-pe-fetch", fetch.__doc__)
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reconstruit la base de données à partir de zéro."
    )
    parser.add_argument(
        "--etudid",
        dest='EID',
        default=None,
        type=int,
        help="Enter l'identifiant ScoDoc d'un étudiant pour uniquement récupérer les informations de cet étudiant."
    )
    parser.add_argument(
        "--semestreid",
        dest='SID',
        default=None,
        type=int,
        help="Enter l'identifiant ScoDoc d'un semestre pour uniquement récupérer les informations des étudiants de ce semestre."
    )
    args = parser.parse_args()

    ######################
    # configuration file #
    ######################
    config = load_config(args.config)

    ################################
    # get/create students database #
    ################################
    database = FileHandler(config["paths"].get("database", "./etudiants.json"))
    if args.reset:
        database.delete()
    try:
        etudiants_resultats = database.load()
    except Exception as e:
        print(f"Initialisation du fichier {database}")
        etudiants_resultats = {}
        database.dump(etudiants_resultats)
    print(f"Base de données: {database}")

    ####################################
    # get list of students from ScoDoc #
    ####################################
    api = ScodocAPI(**config["scodoc"])
    if args.EID:
        print(f"Récupération des données pour l'étudiant {args.EID}")
        etudiants = api.call(f"etudiants/etudid/{args.EID}")
    elif args.SID:
        print(f"Récupération des données pour les étudiants du semestre {args.SID}")
        etudiants = api.call(f"formsemestre/{args.SID}/etudiants")
    else:
        print("Récupération des données pour les étudiants de tous les semestres courants")
        etudiants = api.call("etudiants/courants")


    ###################################################
    # loop over the students to build up the database #
    ###################################################
    for i, e in enumerate(etudiants):
        print(f'{i + 1:03d}/{len(etudiants):03d} {civilite(e["civilite"])} {e["nom"]} {e["prenom"].title()} [{e["id"]}]')

        semestres = api.call(f'etudiant/etudid/{e["id"]}/formsemestres')
        e["semestres"] = []
        for s in semestres:
            print(f'\t{s["titre_num"]} {s["date_debut"]} -> {s["date_fin"]} [{s["formsemestre_id"]}]')
            b = api.call(f'etudiant/etudid/{e["id"]}/formsemestre/{s["id"]}/bulletin')
            s["resultats"] = {k: b[k] for k in ["ues", "ues_capitalisees"]}
            s["groups"] = b["semestre"]["groupes"]
            s["absences"] = b["semestre"]["absences"]
            e["semestres"].append(s)

    etudiants_resultats[str(e["id"])] = e
    database.dump(etudiants_resultats)


def build():
    """ Créé et compile les fiches latex à partir des informations étudiants collectées avec iut-pe-fetch.
    """

    # args parser
    parser = default_parser("iut-pe-build", build.__doc__)
    args = parser.parse_args()

    ######################
    # configuration file #
    ######################
    config = load_config(args.config)

    ####################
    # open students db #
    ####################
    database = FileHandler(config["paths"].get("database", "./etudiants.json"))
    if not database:
        print(f"La base de données {database} n'a pas été trouvée.")
        print(f"Utiliser en premier lieu la commande iut-pe-fetch afin de construire la base de données.\n")
        raise FileNotFoundError("Database not found")
    print(f"Base de données: {database}")
    etudiants = database.load()

    #########################
    # build latex/pdf paths #
    #########################
    latex = FileHandler(config["paths"].get("latex", "latex"), is_file=False)
    latex.create_path()
    print(f"LaTex path: {latex}")
    pdf = FileHandler(config["paths"].get("pdf", "pdf"), is_file=False)
    pdf.create_path()
    print(f"PDF path: {pdf}")

    this_dir = os.path.dirname(os.path.abspath(__file__))
    template = FileHandler([this_dir, "static", "template.tex"])
    logo = FileHandler(config["paths"].get("logo", "logo.png"))
    if logo:
        print(f"Logo: {logo}")
    else:
        print("Le logo n'a pas été trouvé.")
    sign = FileHandler(config["paths"].get("sign", "sign.png"))
    if sign:
        print(f"Signature: {sign}")
    else:
        print("La signature n'a pas été trouvée.")

    ###############################################
    # loop of students to build and compile latex #
    ###############################################
    for i, e in enumerate([v for k, v in etudiants.items()]):
        variables = {
            "titre": "???",
            "parcours": "N/A",
            "alternant": "Non",
            "assiduite": "?",
        }
        print(f'{i + 1:03d}/{len(etudiants):03d} {civilite(e["civilite"])} {e["nom"]} {e["prenom"].title()} [{e["id"]}]', end=" ")

        variables["candidat"] = f'{e["nom"]} {e["prenom"].title()}'
        variables["but"] = e["semestres"][0]["titre_formation"]
        variables["promotion"] = e["semestres"][0]["date_debut"].split("/")[-1]
        max_semester = 0
        abs_inj = 0
        abs_tot = 0
        abs_met = ""

        for ns, s in enumerate(e["semestres"]):
            if s["semestre_id"] == 6:
                continue

            sl = "sem" + "abcde"[s["semestre_id"] - 1]

            ue_key = f'{s["semestre_id"]}' if s["semestre_id"] > 4 else f'UE{s["semestre_id"]}'

            try:
                ue = [s["resultats"]["ues"][f'{ue_key}.{i + 1}']["moyenne"] for i in range(5)]
                d = "/".join(s["date_debut"].split("/")[1:])
                max_semester = max(max_semester, s["semestre_id"])

                variables[sl] = f'S{s["semestre_id"]} {d}'

                variables[sl + "caa"] = ue[0]["value"]
                variables[sl + "cab"] = ue[0]["moy"]
                variables[sl + "cac"] = f'{ue[0]["rang"]}/{ue[0]["total"]}'

                variables[sl + "cba"] = ue[1]["value"]
                variables[sl + "cbb"] = ue[1]["moy"]
                variables[sl + "cbc"] = f'{ue[1]["rang"]}/{ue[1]["total"]}'

                variables[sl + "cca"] = ue[2]["value"]
                variables[sl + "ccb"] = ue[2]["moy"]
                variables[sl + "ccc"] = f'{ue[2]["rang"]}/{ue[2]["total"]}'

                variables[sl + "cda"] = ue[3]["value"]
                variables[sl + "cdb"] = ue[3]["moy"]
                variables[sl + "cdc"] = f'{ue[3]["rang"]}/{ue[3]["total"]}'

                variables[sl + "cea"] = ue[4]["value"]
                variables[sl + "ceb"] = ue[4]["moy"]
                variables[sl + "cec"] = f'{ue[4]["rang"]}/{ue[4]["total"]}'
            except Exception:
                pass


            # ressources
            try:
                variables[sl + "ra"] = s["resultats"]["ues"][f'{ue_key}.{i + 1}']["ressources"][f'MAT{s["semestre_id"]}']["moyenne"]
            except:
                variables[sl + "ra"] = "N/A"
            try:
                variables[sl + "rb"] = s["resultats"]["ues"][f'{ue_key}.{i + 1}']["ressources"][f'COM{s["semestre_id"]}']["moyenne"]
            except:
                variables[sl + "rb"] = "N/A"
            try:
                variables[sl + "rc"] = s["resultats"]["ues"][f'{ue_key}.{i + 1}']["ressources"][f'ANG{s["semestre_id"]}']["moyenne"]
            except:
                variables[sl + "rc"] = "N/A"

            #  get parcours from group name
            for g in [g for g in s["groups"] if g["partition"]["partition_name"] == config["scodoc"].get("groupe", "Parcours")]:
                variables["parcours"] = g["group_name"]

            abs_inj += s["absences"]["injustifie"]
            abs_tot += s["absences"]["total"]
            abs_met = s["absences"]["metrique"].split()[0]

        def _s(n):
            return "s" if n > 1 else ""
        variables["assiduite"] = f'{abs_inj} absence{_s(abs_inj)} injustifiée{_s(abs_inj)} pour {abs_tot} absence{_s(abs_tot)} au total sur {ns + 1} semestres ({abs_met} journée).'

        if max_semester <= 2:
            variables["titre"] = "réorientation BUT 1"
        elif max_semester <= 4:
            variables["titre"] = "réorientation BUT 2"
        elif max_semester <= 6:
            variables["titre"] = "poursuite d'études BUT 3"

        # create latex main file from the template (SED)
        replacements = [
            ("SED_VARIABLES", "".join([f"{chr(92)}def{chr(92)}{k}{{{v}}}\n" for k, v in variables.items()])),
            ("SED_FICHE_NUMBER", str(e["id"])),
            ("SED_ADDRESS", "\\\\\n    ".join(config["latex"]["address"])),
            ("SED_CITY", config["latex"]["city"]),
            ("SED_NAME", config["latex"]["name"])
        ]


        comment = "" if logo else "% "
        replacements.append(("SED_LOGO", f"{comment}{chr(92)}includegraphics[height=2cm]{{{logo.file}}}"))
        comment = "" if sign else "% "
        replacements.append(("SED_SIGN", f"{comment}{chr(92)}includegraphics[height=2cm]{{{sign.file}}}"))

        tex = ""
        with template.read() as f:
            tex = f.read()
            for a, b, in replacements:
                tex = tex.replace(a, b)

        student_tex = FileHandler([latex.path, f'{e["id"]}.tex'])
        with student_tex.write() as f:
            f.write(tex)


        # compile latex
        command = [f'pdflatex -output-directory={latex.path} {student_tex.file} > {student_tex.file}.log']
        subprocess.run(command, shell=True, check=True, text=True)

        # move pdf
        pfrom = os.path.join(latex.path, str(e["id"]) + ".pdf")
        pto = os.path.join(pdf.path, pdf_name(e))
        command = [f'mv {pfrom} {pto}']
        subprocess.run(command, shell=True, check=True, text=True)

        print(f"-> {pto}")



