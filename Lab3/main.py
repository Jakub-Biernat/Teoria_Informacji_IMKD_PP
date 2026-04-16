import math
import random
import sys
from collections import defaultdict

def entropia_znakow(input_text):
    chars = defaultdict(int)
    for char in input_text:
        chars[char] += 1

    probs = {}
    inputlength = len(input_text)
    for char in chars:
        probs[char] = chars[char] / inputlength

    entropy = 0
    for prob in probs:
        entropy += -1 * probs[prob] * math.log(probs[prob], 2)

    return entropy



if __name__ == '__main__':
    input_file = sys.argv[1]
    input_text = open(input_file, "r").read()
    print(entropia_znakow(input_text))

