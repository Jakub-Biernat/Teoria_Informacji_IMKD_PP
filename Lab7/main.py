import math
import os
from bitarray import bitarray

def create():
    return {bytes([i]): i for i in range(256)}

def encode(data, max_dict_size=None):
    codebook = create()
    string = bytes([data[0]])
    next_code = 256
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
    codebook = create()
    reverse_codebook = {code: symbol for symbol, code in codebook.items()}
    next_code = 256

    old = data[0]
    result = bytearray(reverse_codebook[old])
    c = b""
    #c = reverse_codebook[old][:1]

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
    bits = bitarray(endian="big")

    bits.frombytes(len(encoded).to_bytes(4, "big"))
    next_code = 256

    for code in encoded:
        b = bits_required(next_code)
        bits.extend(format(code, f"0{b}b"))
        next_code += 1

    with open(filename, "wb") as f:
        bits.tofile(f)

def load(filename):
    bits = bitarray(endian="big")

    with open(filename, "rb") as f:
        bits.fromfile(f)

    size = int.from_bytes(bits[:32].tobytes(), "big")
    encoded = []

    pos = 32
    next_code = 256

    for _ in range(size):
        b = bits_required(next_code)

        code = int(bits[pos:pos + b].to01(), 2)
        encoded.append(code)

        pos += b
        next_code += 1

    return encoded

def verify(original, decoded):
    return original == decoded

def bits_required(code):
    return max(8, math.ceil(math.log2(code + 1)))

def test_LZW(filename, max_dict_size=None):
    data = open(filename, "rb").read()

    encoded = encode(data, max_dict_size)

    compressed_file = "compressed.txt"
    save(compressed_file, encoded)

    loaded = load(compressed_file)
    decoded = decode(loaded, max_dict_size)

    print(f"\nPlik: {filename}")

    if verify(data, decoded):
        print("Kompresja przeprowadzona pomyslnie")
    else:
        print("Niepowodzenie")
        return

    original_size = os.path.getsize(filename) * 8
    compressed_size = os.path.getsize(compressed_file) * 8

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

if __name__ == "__main__":
    filenames = [
        "norm_wiki_sample.txt",
        "wiki_sample.txt",
        "lena.bmp"
    ]

    for filename in filenames:
        test_LZW(filename)
        test_LZW(filename, 2 ** 12)
        test_LZW(filename, 2 ** 18)