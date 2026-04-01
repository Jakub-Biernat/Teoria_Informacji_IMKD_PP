from collections import defaultdict
import random

def generator_zerowego_rzedu(input, size, outputfile):
    text = ""
    for _ in range(size):
        text += random.choice(input)

    with open(outputfile, "w") as f:
        f.write(text)
        f.close()

    #Srednia dlugosc slowa wynosi 26

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

    #W moim wypadku srednia dlugosc slowa wyniosla okolo 5, a srednia dlugosc slowa
    #norm_hamlet.txt wynosi okolo 4, wiec sa przyblizone