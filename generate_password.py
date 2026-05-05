import hashlib
import argparse

def _hash(password: str) -> str:
    md5_hex = hashlib.md5(password.encode("utf-8")).hexdigest()
    sha512_hex = hashlib.sha512(md5_hex.encode("utf-8")).hexdigest()
    return sha512_hex



parser = argparse.ArgumentParser()
parser.add_argument("password", help="Mot de passe à hasher")
args = parser.parse_args()

password:str = args.password


print(_hash(password))
