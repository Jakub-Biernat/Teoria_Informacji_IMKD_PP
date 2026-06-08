import math
from sys import argv
from bitarray import bitarray
import json
from collections import Counter, defaultdict

def create():
    codebook = {bytes([i]): i for i in range(256)}
    return codebook

def encode(text):
    codebook = create()
    string = bytes([text[0]])
    next_code = max(codebook.values()) + 1
    encoded = []
    for byte in text[1:]:
        char = bytes([byte])
        if string + char in codebook:
            string = string + char
        else:
            encoded.append(codebook[string])
            codebook[string + char] = next_code
            next_code += 1
            string = char

    encoded.append(codebook[string])
    return encoded

def decode(text):
    result = bytearray()
    codebook = create()
    reverse_codebook = {code: symbol for symbol, code in codebook.items()}
    next_code = max(reverse_codebook.keys()) + 1

    c = b""
    old = text[0]
    result.extend(reverse_codebook[old])

    for new in text[1:]:
        if new in reverse_codebook:
            word = reverse_codebook[new]
        else:
            word = reverse_codebook[old] + c
        result.extend(word)
        c = word[:1]
        reverse_codebook[next_code] = reverse_codebook[old] + c
        next_code += 1
        old = new

    return bytes(result)

def save(filename, encoded):
    data = {
        "encoded": encoded
    }

    with open(filename, "w") as f:
        json.dump(data, f)

def load(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    encoded = data["encoded"]

    return encoded

def verify(original, decoded):
    return original == decoded

if __name__ == '__main__':
    #Run: py .\main.py textToCompress.txt compressed.json
    text = open(argv[1], "rb").read()

    encoded_1 = encode(text)
    save(argv[2], encoded_1)

    encoded_2 = load(argv[2])
    decoded = decode(encoded_2)

    if verify(text, decoded):
        print("Kompresja przeprowadzona pomyslnie")
    else:
        print("Niepowodzenie")

    original_size = len(text) * 8
    bits_per_code = math.ceil(math.log2(max(encoded_1) + 1))
    compressed_size = len(encoded_1) * bits_per_code

    print(f"\nOryginalny rozmiar: {original_size} bitów")
    print(f"Rozmiar po kompresji: {compressed_size} bitów")

    ratio = compressed_size / original_size

    print(f"Stopień kompresji: {ratio:.2f}")
    print(f"Oszczędność: {(1 - ratio) * 100:.2f}%")
