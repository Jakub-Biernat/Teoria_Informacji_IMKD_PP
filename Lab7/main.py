import math
from sys import argv
from bitarray import bitarray
import json
from collections import Counter, defaultdict

def create():
    codebook = {bytes([i]): i for i in range(256)}
    return codebook

def encode(data, max_dict_size=None):
    codebook = create()
    string = bytes([data[0]])
    next_code = max(codebook.values()) + 1
    encoded = []
    for byte in data[1:]:
        char = bytes([byte])
        if string + char in codebook:
            string += char
        else:
            encoded.append(codebook[string])
            if max_dict_size is None or next_code < max_dict_size:
                codebook[string + char] = next_code
                next_code += 1
            string = char

    encoded.append(codebook[string])
    return encoded

def decode(data, max_dict_size=None):
    result = bytearray()
    codebook = create()
    reverse_codebook = {code: symbol for symbol, code in codebook.items()}
    next_code = max(reverse_codebook.keys()) + 1

    c = b""
    old = data[0]
    result.extend(reverse_codebook[old])

    for new in data[1:]:
        if new in reverse_codebook:
            word = reverse_codebook[new]
        else:
            word = reverse_codebook[old] + c
        result.extend(word)
        c = word[:1]
        if max_dict_size is None or next_code < max_dict_size:
            reverse_codebook[next_code] = reverse_codebook[old] + c
            next_code += 1
        old = new

    return bytes(result)

def save(filename, encoded):
    with open(filename, "w") as f:
        json.dump(encoded, f)

def load(filename):
    with open(filename, "r") as f:
        return json.load(f)

def verify(original, decoded):
    return original == decoded

def compressed_size_bits(encoded):
    bits_per_code = math.ceil(math.log2(max(encoded) + 1))
    return len(encoded) * bits_per_code

def test_LZW(filename, max_dict_size=None):
    data = open(filename, "rb").read()
    encoded = encode(data, max_dict_size)
    compressed_file = "compressed.json"
    save(compressed_file, encoded)
    loaded = load(compressed_file)
    decoded = decode(loaded, max_dict_size)

    if verify(data, decoded):
        print("Kompresja przeprowadzona pomyslnie")
    else:
        print("Niepowodzenie")
        return

    original_size = len(data) * 8
    compressed_size = compressed_size_bits(encoded)

    ratio = compressed_size / original_size if original_size else 0

    if max_dict_size is None:
        print("Limit słownika: brak")
    else:
        print(f"Limit słownika: {max_dict_size}")

    print(f"Oryginalny rozmiar: {original_size} bitów")
    print(f"Rozmiar po kompresji: {compressed_size} bitów")

    print(f"Stopień kompresji: {ratio:.2f}")
    print(f"Oszczędność: {(1-ratio)*100:.2f}%")
    print("-" * 30)

if __name__ == '__main__':
    filenames = [
        "norm_wiki_sample.txt",
        "wiki_sample.txt",
        "lena.bmp"
    ]

    for filename in filenames:
        print(f"Plik: {filename}", end="")
        print("\n=== Bez limitu słownika ===")
        test_LZW(filename)
        print("\n=== Limit 2^12 ===")
        test_LZW(filename, 2 ** 12)
        print("\n=== Limit 2^18 ===")
        test_LZW(filename, 2 ** 18)
