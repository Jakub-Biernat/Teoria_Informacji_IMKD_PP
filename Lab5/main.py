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

    L = len(next(iter(codebook.values())))

    return codebook, encoded

def verify(original, decoded):
    return original == decoded

if __name__ == '__main__':
    text = open(argv[1], "r").read()
    freq = Counter(text)

    #Test