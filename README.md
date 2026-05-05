# StarLoco Tooling

Petits scripts utilitaires pour manipuler et explorer des données liées au serveur StarLoco (Python + SQL).

## Prérequis

- Python 3.10+
- Accès à une base MySQL/MariaDB StarLoco

## Installation

```bash
python -m venv venv
pip install -r requirements.txt
```

## Configuration

Modifier `config.py` avec les identifiants de ta base de données (`host`, `port`, `user`, `password`, `database`).

## Utilisation

Il est recommandé de simplement lancer le menu.py qui sert de launcher pour le reste.

```bash
python menu.py
```

### Explorer questions/reponses NPC

```bash
python reponses_possible_dialogue.py question 123
python reponses_possible_dialogue.py reponse 456
python reponses_possible_dialogue.py chercher "texte"
```

### SQL utile

- `sql/add_account.sql` : template d'insertion d'un compte dans `starloco_login.world_accounts`.

## Notes

- `text_clean.py` contient des fonctions pour corriger des problemes d'encodage (mojibake) et normaliser les retours a la ligne.
