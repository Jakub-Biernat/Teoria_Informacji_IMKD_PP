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

    return codebook, L

def encode(text, codebook):
    bits = bitarray()

    for char in text:
        bits.extend(codebook[char])

    return bits


if __name__ == '__main__':
    text = "hello hello world"
    freq = Counter(text)

    codebook, reverse, L = create(freq)
    print(reverse)