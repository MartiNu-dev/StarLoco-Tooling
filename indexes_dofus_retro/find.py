#!/usr/bin/env python3

from pathlib import Path
import argparse


def main(texte:str, find_in_dialogues:bool=False):
    # parser = argparse.ArgumentParser()
    # parser.add_argument("texte", help="Texte à rechercher")
    # args = parser.parse_args()

    # texte:str = args.texte.lower()


    for fichier in Path("D:\\Travaux\\Jeux\\Server_dofus\\indexes_dofus_retro\\").iterdir():
        if not fichier.is_file():
            continue

        if not find_in_dialogues:
            if fichier.name.startswith("dialogue"):
                continue

        try:
            with fichier.open("r", encoding="utf-8", errors="ignore") as f:
                for num, ligne in enumerate(f, start=1):
                    if texte.lower() in ligne.lower():
                        print(f"\n{fichier}  -  {ligne}", end="")
        except OSError:
            pass
    print("\n\nRecherche terminee.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("texte", help="Texte à rechercher")

    parser.add_argument("--dialogues", action="store_true", help="Rechercher dans les dialogues")
    args = parser.parse_args()

    texte:str = args.texte.lower()
    find_in_dialogues:bool = args.dialogues


    if not texte:
        print("Usage : find.py <texte> [--dialogues]")
        exit(1)

    main(texte, find_in_dialogues=find_in_dialogues)