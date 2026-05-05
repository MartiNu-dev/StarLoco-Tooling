
import argparse

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"

def decode_char(c: str) -> int:
    return ALPHABET.index(c)

def decode_2_char(code: str) -> int:
    return decode_char(code[0]) * 64 + decode_char(code[1])

def decode_1_char(c: str) -> int:
    return decode_char(c)



if __name__ == "__main__":
    # on parse les arguments 'decode_2_char' ou 'decode_1_char'
    parser = argparse.ArgumentParser(description="Decode a protocole code")
    parser.add_argument("function", choices=["decode_2_char", "decode_1_char"], help="The function to use for decoding")
    parser.add_argument("code", help="The code to decode")

    args = parser.parse_args()
    if args.function == "decode_2_char":
        print(decode_2_char(args.code))
    elif args.function == "decode_1_char":
        print(decode_1_char(args.code))
