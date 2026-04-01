import random
import sys
from collections import defaultdict


def generator_zerowego_rzedu(input, size, outputfile):
    text = ""
    for _ in range(size):
        text += random.choice(input)

    with open(outputfile, "w") as f:
        f.write(text)
        f.close()

def generator_pierwszego_rzedu(input, size, outputfile):
    chars = defaultdict(int)
    for char in input:
        chars[char] += 1

    probs = {}
    inputlength = len(input)
    for char in chars:
        probs[char] = chars[char] / inputlength

    keys = list(probs.keys())
    weights = list(probs.values())
    text = "".join(random.choices(keys, weights, k=size))

    with open(outputfile, "w") as f:
        f.write(text)
        f.close()

def generator_markova_pierwszego_rzedu(input, size, outputfile):
    chars = defaultdict(int)
    for char in input:
        chars[char] += 1

    probs = {}
    inputlength = len(input)
    for char in chars:
        probs[char] = chars[char] / inputlength

    bigrams = []
    for i in range(inputlength - 1):
        bigrams.append(text[i:i + 2])

    keys = list(probs.keys())
    weights = list(probs.values())
    text = "".join(random.choices(keys, weights, k=1))

    with open(outputfile, "w") as f:
        f.write(text)
        f.close()

if _name_ == '_main_':
    inputfile = sys.argv[1]
    input = open(inputfile, "r").read()
    size = int(sys.argv[2])
    outputfile = sys.argv[3]

    #Generator zerowego rzedu
    #generator_zerowego_rzedu(input, size, outputfile)
    #Generator pierwszego rzedu
    generator_pierwszego_rzedu(input, size, outputfile)