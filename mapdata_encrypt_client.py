#!/usr/bin/env python3
"""
Encrypt Dofus / StarLoco client mapData from plain hashed form to the SWF hex form.

This implements the inverse of the decrypt logic used around StarLoco-style map handling:
- prepare key from the hex key string
- compute checksum-derived offset
- XOR each plaintext character with the rolling key character
- emit lowercase hex

It also includes the matching decrypt function so you can round-trip test.
"""
from __future__ import annotations

import argparse
import sys
import urllib.parse
from pathlib import Path


def prepare_key(hex_key: str) -> str:
    raw = bytes.fromhex(hex_key)
    return urllib.parse.unquote(raw.decode("utf-8"))


def checksum_key(data: str) -> str:
    total = 0
    for ch in data:
        total += ord(ch) % 16
    return "0123456789ABCDEF"[total % 16]


def decrypt_map_data(cipher_hex: str, key_hex: str) -> str:
    prepared_key = prepare_key(key_hex)
    checksum = int(checksum_key(prepared_key), 16) * 2

    chars = []
    for i in range(0, len(cipher_hex), 2):
        sub = cipher_hex[i:i + 2]
        num = int(sub, 16)
        s = int(round((((i) / 2) + checksum) % len(prepared_key)))
        key_char = ord(prepared_key[s:s + 1])
        chars.append(chr(num ^ key_char))

    return "".join(chars).encode("utf-8", "surrogatepass").decode("unicode_escape")


def encrypt_map_data(plain_mapdata: str, key_hex: str) -> str:
    prepared_key = prepare_key(key_hex)
    checksum = int(checksum_key(prepared_key), 16) * 2

    out = []
    for idx, ch in enumerate(plain_mapdata):
        s = int(round((idx + checksum) % len(prepared_key)))
        key_char = ord(prepared_key[s:s + 1])
        encoded = ord(ch) ^ key_char
        out.append(f"{encoded:02x}")
    return "".join(out)


def load_input(args: argparse.Namespace) -> str:
    if args.mapdata is not None:
        return args.mapdata.strip()
    return Path(args.mapdata_file).read_text(encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Encrypt plain hashed mapData to the client SWF hex format."
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--mapdata", help="plain mapData string such as Hhaaeaaaaa...")
    src.add_argument("--mapdata-file", help="file containing the plain mapData string")
    parser.add_argument("--key", required=True, help="maps.key hex string")
    parser.add_argument("--verify", action="store_true", help="decrypt the result and verify a round-trip")
    parser.add_argument("--output", help="optional output file for the encrypted hex")
    args = parser.parse_args()

    plain = load_input(args)
    encrypted = encrypt_map_data(plain, args.key)

    if args.verify:
        round_trip = decrypt_map_data(encrypted, args.key)
        if round_trip != plain:
            print("Round-trip verification failed.", file=sys.stderr)
            print(f"expected: {plain[:120]}{'...' if len(plain) > 120 else ''}", file=sys.stderr)
            print(f"got     : {round_trip[:120]}{'...' if len(round_trip) > 120 else ''}", file=sys.stderr)
            return 2

    if args.output:
        Path(args.output).write_text(encrypted, encoding="utf-8")

    print(encrypted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
