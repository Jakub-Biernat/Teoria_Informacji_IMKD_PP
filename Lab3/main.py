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
    for prob in probs.values():
        entropy += -1 * prob * math.log(prob, 2)

    return entropy

def entropia_slow(input_text):
    words = defaultdict(int)
    input_words = input_text.split()
    for word in input_words:
        words[word] += 1

    probs = {}
    inputlength = len(input_words)
    for word in words:
        probs[word] = words[word] / inputlength

    entropy = 0
    for prob in probs.values():
        entropy += -1 * prob * math.log(prob, 2)

    return entropy



if __name__ == '__main__':
    input_file = sys.argv[1]
    input_text = open(input_file, "r").read()
    print(entropia_slow(input_text))

