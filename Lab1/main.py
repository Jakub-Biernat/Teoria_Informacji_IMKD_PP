import random
import sys
from collections import defaultdict

def generator_markova_pierwszego_rzedu(input, size, outputfile):
    chars = defaultdict(int)
    for char in input:
        chars[char] += 1

    probs = {}
    inputlength = len(input)
    for char in chars:
        probs[char] = chars[char] / inputlength

    bigrams = defaultdict(int)
    for i in range(inputlength - 1):
        bigrams[input[i:i + 2]] += 1

    bigram_probs = {}
    for bigram in bigrams:
        bigram_probs[bigram] = bigrams[bigram] / (inputlength - 1)



    keys = list(probs.keys())
    weights = list(probs.values())
    text = "".join(random.choices(keys, weights, k=1))

    with open(outputfile, "w") as f:
        f.write(text)
        f.close()

if __name__ == '__main__':
    inputfile = sys.argv[1]
    input = open(inputfile, "r").read()
    size = int(sys.argv[2])
    outputfile = sys.argv[3]

    #Generator Markova pierwszego rzedu
    generator_markova_pierwszego_rzedu(input, size, outputfile)