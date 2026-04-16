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

def entropia_znakow_warunkowa(input_text, order):
    inputlength = len(input_text)

    #Slownik n-gramow bez zliczania, do pradopodobienstwa lacznego
    joint_n_grams = defaultdict(int)
    #Slownik n-gramow, zliczanie ile razy po danym ciagu znakow wystepuje inny znak
    n_grams = defaultdict(lambda: defaultdict(int))
    for i in range(inputlength - order):
        joint_n_grams[input_text[i : i + order + 1]] += 1
        n_grams[input_text[i : i + order]][input_text[i + order]] += 1

    #prawdopodobienstwo laczne
    joint_probs = {}
    total_joint_n_grams = sum(joint_n_grams.values())
    for n_gram in joint_n_grams:
        joint_probs[n_gram] = joint_n_grams[n_gram] / total_joint_n_grams

    #Rozklad prawdopodobienstwa wystapienia kolejnego znaku dla kazdego n-gramu
    n_grams_probs = {}
    for first_chars in n_grams:
        total = sum(n_grams[first_chars].values())
        n_grams_probs[first_chars] = {
            next_char: count / total
            for next_char, count in n_grams[first_chars].items()
        }
    print(n_grams_probs)
    print(joint_probs)



if __name__ == '__main__':
    input_file = sys.argv[1]
    input_text = open(input_file, "r").read()
    print(entropia_znakow_warunkowa(input_text, 1))

