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


def civilite(c):
    return "Mme" if c == "F" else "Mr"


def pdf_name(e):
    """ Define the name of the PDF file based on student data
    """
    name = "_".join([_ for _ in e["nom"].split()])
    surname = "_".join([_.title() for _ in e["prenom"].split()])
    return f'{name}_{surname}_{e["id"]}.pdf'

def default_parser(prog, doc):
    import argparse

    parser = argparse.ArgumentParser(
        prog=prog,
        description=doc,
        epilog="Yolo"
    )
    parser.add_argument(
        "--config",
        default="config.yml",
        type=str,
        help="Chemin vers le fichier de configuration (défaut: répertoire courant)."
    )
    return parser

def load_config(path):
    f = FileHandler(path)
    if not f:
        print(f"Le fichier de configuration n'a pas été trouvé à l'emplacement {f}.")
        print("Vérifier le chemin et utiliser l'option --config si besoin.\n")
        raise FileNotFoundError("File not found")

    c = f.load()
    if c.get("paths") is None:
        c["paths"] = {}

    return c

class FileHandler:
    def __init__(self, path, is_file=True):
        from pathlib import Path
        import os

        if isinstance(path, list):
            path = os.path.join(*path)

        path = Path(path).expanduser().resolve()
        self.is_file = is_file
        if is_file:
            self.file = path
            path, _ = os.path.split(path)
            self.path = Path(path)
        else:
            self.file = None
            self.path = Path(path)

    def __str__(self):
        if self.file:
            return str(self.file)
        else:
            return str(self.path)

    def __bool__(self):
        if self.file:
            return self.file.exists()
        else:
            return self.path.exists()

    def create_path(self):
        if self:
            return
        self.path.mkdir(parents=True)

    def delete(self):
        print(f"Suppression du fichier {self.file}")
        if self:
            self.file.unlink()

    def read(self):
        if not self.is_file:
            return None
        return open(self.file, "r")

    def write(self):
        if not self.is_file:
            return None
        return open(self.file, "w")

    def dump(self, data):
        import json
        json.dump(data, self.write(), indent=4)

    def load(self):
        import json
        import yaml
        ext = str(self.file).split(".")[-1]
        if ext not in ["yml", "json"]:
            raise NotImplementedError(f"Extension {ext} not handled yet by the file handler for loading data.")

        if ext == "json":
            return json.load(self.read())
        elif ext == "yml":
            return yaml.safe_load(self.read())


