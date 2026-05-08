import math
import random
import string
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

    entropy = 0
    for n_gram, joint_prob in joint_probs.items():
        current_chars = n_gram[:-1]
        next_char = n_gram[-1]

        cond_prob = n_grams_probs[current_chars][next_char]

        entropy += -1 * joint_prob * math.log(cond_prob, 2)

    return entropy

def entropia_slow_warunkowa(input_text, order):
    words = input_text.split()
    inputlength = len(words)

    # Slownik n-gramow bez zliczania, do pradopodobienstwa lacznego
    joint_n_grams = defaultdict(int)
    # Slownik n-gramow, zliczanie ile razy po danym ciagu slow wystepuje inne slowo
    n_grams = defaultdict(lambda: defaultdict(int))

    for i in range(inputlength - order):
        current_words = tuple(words[i : i + order])
        next_word = words[i + order]

        joint_n_grams[tuple(words[i : i + order + 1])] += 1
        n_grams[current_words][next_word] += 1

    # prawdopodobiesstwo laczne
    joint_probs = {}
    total_joint_n_grams = sum(joint_n_grams.values())
    for n_gram in joint_n_grams:
        joint_probs[n_gram] = joint_n_grams[n_gram] / total_joint_n_grams

    #Rozklad prawdopodobienstwa wystapienia kolejnego slowa dla kazdego n-gramu
    n_grams_probs = {}
    for current_words in n_grams:
        total = sum(n_grams[current_words].values())
        n_grams_probs[current_words] = {
            word: count / total
            for word, count in n_grams[current_words].items()
        }

    entropy = 0
    for n_gram, joint_prob in joint_probs.items():
        current_words = n_gram[:-1]
        next_words = n_gram[-1]

        cond_prob = n_grams_probs[current_words][next_words]

        entropy += -1 * joint_prob * math.log2(cond_prob)

    return entropy

def test_entropies(text):
    entropies = {}

    entropies["H_char"] = entropia_znakow(text)

    for order in range(1, 6):
        entropies[f"H_char_cond{order}"] = entropia_znakow_warunkowa(text, order)

    entropies["H_word"] = entropia_slow(text)

    for order in range(1, 6):
        entropies[f"H_word_cond{order}"] = entropia_slow_warunkowa(text, order)

    return entropies

def print_entropies(file):
    text = open(file, "r").read()
    text = text[:10000]
    results = test_entropies(text)
    for entropy_name, entropy_value in results.items():
        print(f"{entropy_name}: {entropy_value}")

    print()

if __name__ == '__main__':
    chars = string.ascii_lowercase + string.digits + " "
    random_text = "".join(random.choice(chars) for _ in range(2000))

    with open("test.txt", "w") as test_file:
        test_file.write(random_text)

    test_samp_files = [
        "sample0.txt",
        "sample1.txt",
        "sample2.txt",
        "sample3.txt",
        "sample4.txt",
        "sample5.txt",
        "test.txt" #dla sprawdzenia dla na pewno nie naturalnego jezyka
    ]

    #norm_wiki_en
    print("Test entropii dla pliku norm_wiki_en.txt")
    print_entropies("norm_wiki_en.txt")

    #norm_wiki_en
    print("Test entropii dla pliku norm_wiki_la.txt")
    print_entropies("norm_wiki_la.txt")

    #samples
    for file in test_samp_files:
        print(f"Test entropii dla pliku {file}")
        print_entropies(file)

    #sample1 oraz sample3 są językami naturalnymi


