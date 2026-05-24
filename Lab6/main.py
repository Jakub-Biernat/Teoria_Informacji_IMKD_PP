import math
from sys import argv
from bitarray import bitarray
import json
from collections import Counter, defaultdict
import heapq

class Node:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_codes(node, prefix, codebook):
    if node.symbol is not None:
        codebook[node.symbol] = prefix if prefix else "0"
        return codebook

    build_codes(node.left, prefix + "0", codebook)
    build_codes(node.right, prefix + "1", codebook)

    return codebook

def create(frequencies):
    huffmans_tree = []

    for symbol, freq in frequencies.items():
        heapq.heappush(huffmans_tree, Node(symbol, freq))

    while len(huffmans_tree) > 1:
        leftNode = heapq.heappop(huffmans_tree)
        rightNode = heapq.heappop(huffmans_tree)

        mergedNode = Node(freq=leftNode.freq + rightNode.freq)
        mergedNode.left = leftNode
        mergedNode.right = rightNode

        heapq.heappush(huffmans_tree, mergedNode)

    rootNode = huffmans_tree[0]
    codebook = {}
    codebook = build_codes(rootNode, "", codebook)

    return codebook

def encode(text, codebook):
    bits = bitarray()

    for char in text:
        bits.extend(codebook[char])

    return bits

def decode(bits, codebook):
    result = []
    reverse_codebook = {code: symbol for symbol, code in codebook.items()}

    current_code = ""
    for bit in bits:
        current_code += str(bit)
        if current_code in reverse_codebook:
            result.append(reverse_codebook[current_code])
            current_code = ""

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

def average_codeword_length(codebook, frequencies):
    total = sum(frequencies.values())

    L = 0
    for symbol in frequencies:
        prob = frequencies[symbol] / total
        length = len(codebook[symbol])
        L += prob * length

    return L

def symbol_entropy(input_text):
    chars = defaultdict(int)
    for char in input_text:
        chars[char] += 1

    probs = {}
    inputlength = len(input_text)
    for char in chars:
        probs[char] = chars[char] / inputlength

    entropy = 0
    for prob in probs.values():
        entropy += -1 * prob * math.log(prob, 2)

    return entropy


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

    L = average_codeword_length(codebook_1, freq)
    print(f"Średnia długość słów kodowych: {L:.2f}")

    H = symbol_entropy(text)
    Eff = H / L
    print(f"Efektywność kodowania: {Eff:.2f}")

