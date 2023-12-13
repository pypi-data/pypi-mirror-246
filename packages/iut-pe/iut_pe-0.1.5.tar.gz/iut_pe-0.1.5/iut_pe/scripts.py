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
from iut_pe.helpers import civilite, pdf_name, FileHandler, default_parser, load_config, is_float, handle_accents
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
    parser.add_argument(
        "--skip",
        action="store_true",
        help="Ignore les pdf déjà présents."
    )
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
    for etudiant_i, e in enumerate([v for k, v in etudiants.items()]):
        print(f'{etudiant_i + 1:03d}/{len(etudiants):03d} {civilite(e["civilite"])} {e["nom"]} {e["prenom"].title()} [{e["id"]}]', end=" ")

        # PDF files
        pdf_from = os.path.join(latex.path, str(e["id"]) + ".pdf")
        pdf_to = os.path.join(pdf.path, pdf_name(e))

        if bool(FileHandler(pdf_to)) and args.skip:
            print(f" déjà compilé")
            continue

        # variables to define in latex template
        variables = {
            "titre": "???",
            "parcours": "N/A",
            "alternant": "Non",
            "assiduite": "?",
        }

        variables["candidat"] = f'{e["nom"]} {e["prenom"].title()}'
        variables["but"] = e["semestres"][0]["titre_formation"]
        variables["promotion"] = e["semestres"][0]["date_debut"].split("/")[-1]
        max_semester = 0
        abs_inj = 0
        abs_tot = 0
        abs_met = ""
        parcours = []
        semesters = []

        for ns, s in enumerate(e["semestres"]):

            # get BC (should be the same for all semesters)
            for a, bc in zip("abcde", s["parcours"][0]["annees"]["1"]["competences"].keys()):
                variables["bc" + a] = bc

            sl = "sem" + "abcdef"[s["semestre_id"] - 1]
            sdate = "/".join(sorted(list(set([s["date_debut"].split("/")[-1], s["date_fin"].split("/")[-1]]))))
            sdate = s["annee_scolaire"]
            semesters.append(f'S{s["semestre_id"]} {sdate}')

            ue_key = f'{s["semestre_id"]}' if s["semestre_id"] > 4 else f'UE{s["semestre_id"]}'

            # try:
            ues = [s["resultats"]["ues"].get(f'{ue_key}.{i + 1}', {}).get("moyenne") for i in range(5)]
            d = "/".join(s["date_debut"].split("/")[1:])
            max_semester = max(max_semester, s["semestre_id"])

            variables[sl] = f'S{s["semestre_id"]} {sdate}'

            for a, ue in zip("abcde", ues):
                if ue is None:
                    variables[sl + "c" + a + "a"] = "N/A"
                    variables[sl + "c" + a + "b"] = "N/A"
                    variables[sl + "c" + a + "c"] = "N/A"
                else:
                    variables[sl + "c" + a + "a"] = ue["value"] if is_float(ue["value"]) else "N/A"
                    variables[sl + "c" + a + "b"] = ue["moy"] if is_float(ue["moy"]) else "N/A"
                    variables[sl + "c" + a + "c"] = f'{ue["rang"]}/{ue["total"]}' if ue["total"] else "N/A"

            # ressources
            for a, RES in zip("abc", ["MAT", "COM", "ANG"]):
                if f'{ue_key}.1' not in s["resultats"]["ues"]:
                    note = "N/A"
                elif f'{RES}{s["semestre_id"]}' not in s["resultats"]["ues"][f'{ue_key}.1']["ressources"]:
                    note = "N/A"
                else:
                    note = s["resultats"]["ues"][f'{ue_key}.1']["ressources"][f'{RES}{s["semestre_id"]}'].get("moyenne")
                variables[sl + "r" + a] = note if is_float(note) else "N/A"

            #  get parcours from group name
            if len(s["parcours"]) == 1:
                # get parcours from s["parcours"]
                parcours.append(handle_accents(s["parcours"][0]["libelle"]))
            else:
                # get parcours from group
                for g in [g for g in s["groups"] if g["partition"]["partition_name"] == config["scodoc"].get("groupe", "Parcours")]:
                    parcours.append(handle_accents(g["group_name"]))

            variables["parcours"] = " - ".join(list(set(parcours)))
            variables["semestres"] = ", ".join(semesters)
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

        command = [f'pdflatex -halt-on-error -output-directory={latex.path} {student_tex.file} > {student_tex.file}.log']
        subprocess.run(command, shell=True, check=True, text=True)

        # move pdf
        command = [f'mv {pdf_from} {pdf_to}']
        subprocess.run(command, shell=True, check=True, text=True)

        print(f"-> {pdf_to}")



