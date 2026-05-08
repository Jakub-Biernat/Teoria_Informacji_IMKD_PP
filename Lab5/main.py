from sys import argv
from bitarray import bitarray
import json
import math
from collections import Counter

def create(frequencies):
    symbols = list(frequencies.keys())
    n = len(symbols)

    L = math.ceil(math.log2(n)) if n > 1 else 1

    codebook = {}

    for i, symbol in enumerate(symbols):
        code = format(i, f'0{L}b')
        codebook[symbol] = code

    return codebook

def encode(text, codebook):
    bits = bitarray()

    for char in text:
        bits.extend(codebook[char])

    return bits

def decode(bits, codebook):
    result = []
    reverse_codebook = {code: symbol for symbol, code in codebook.items()}

    L = len(next(iter(codebook.values())))

    for i in range(0, len(bits), L):
        chunk = bits[i:i+L].to01()
        result.append(reverse_codebook[chunk])

    return ''.join(result)

def save(filename, codebook, encoded_bits):
    data = {
        "codebook": codebook,
        "encoded": encoded_bits.to01()
    }

    with open(filename, "w") as f:
        json.dump(data, f)

def load(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    codebook = data["codebook"]
    encoded = bitarray(data["encoded"])

    return codebook, encoded

def verify(original, decoded):
    return original == decoded

if __name__ == '__main__':
    #Run: py .\main.py textToCompress.txt compressed.json
    text = open(argv[1], "r").read()
    freq = Counter(text)

    codebook_1 = create(freq)
    encoded_bits_1 = encode(text, codebook_1)
    save(argv[2], codebook_1, encoded_bits_1)

    codebook_2, encoded_bits_2 = load(argv[2])
    decoded = decode(encoded_bits_2, codebook_2)

    if verify(text, decoded):
        print("Kompresja przeprowadzona pomyslnie")
    else:
        print("Niepowodzenie")

    original_size = len(text) * 8
    compressed_size = len(encoded_bits_1)

    print(f"\nOryginalny rozmiar: {original_size} bitów")
    print(f"Rozmiar po kompresji: {compressed_size} bitów")

    ratio = compressed_size / original_size

    print(f"Stopień kompresji: {ratio:.2f}")
    print(f"Oszczędność: {(1 - ratio) * 100:.2f}%")
