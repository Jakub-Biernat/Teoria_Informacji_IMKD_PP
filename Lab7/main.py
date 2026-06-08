import math
from sys import argv
from bitarray import bitarray
import json
from collections import Counter, defaultdict

def create(frequencies):
    codebook = {item: i for i, item in enumerate(frequencies.keys())}
    return codebook

def encode(text, codebook):
    string = text[0]
    next_code = max(codebook.values()) + 1
    encoded = []
    for char in text[1:]:
        if string + char in codebook:
            string = string + char
        else:
            encoded.append(codebook[string])
            codebook[string + char] = next_code
            next_code += 1
            string = char

    encoded.append(codebook[string])
    return encoded

def decode(text, frequencies):
    result = []
    codebook = create(frequencies)
    reverse_codebook = {code: symbol for symbol, code in codebook.items()}
    next_code = max(reverse_codebook.keys()) + 1

    c = ""
    old = text[0]
    result.append(reverse_codebook[old])

    for new in text[1:]:
        if new in reverse_codebook:
            word = reverse_codebook[new]
        else:
            word = reverse_codebook[old] + c
        result.append(word)
        c = word[0]
        reverse_codebook[next_code] = reverse_codebook[old] + c
        next_code += 1
        old = new

    return "".join(result)

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
    text = open(argv[1], "r").read()
    freq = Counter(text)

    codebook_1 = create(freq)
    encoded_1 = encode(text, codebook_1)
    save(argv[2], encoded_1)

    encoded_2 = load(argv[2])
    decoded = decode(encoded_2, freq)

    if verify(text, decoded):
        print("Kompresja przeprowadzona pomyslnie")
    else:
        print("Niepowodzenie")

