import random
import sys
from collections import defaultdict

def generator_markova(input_text, size, outputfile, order):
    chars = defaultdict(int)
    for char in input_text:
        chars[char] += 1

    inputlength = len(input_text)
    probs = {char: total / inputlength for char, total in chars.items()}

    n_grams = defaultdict(lambda: defaultdict(int))
    for i in range(inputlength - order):
        n_grams[input_text[i:i+order]][input_text[i + order]] += 1

    n_grams_probs = {}
    for first_chars in n_grams:
        total = sum(n_grams[first_chars].values())
        n_grams_probs[first_chars] = {
            next_char: count / total
            for next_char, count in n_grams[first_chars].items()
        }

    random_index = random.randint(0, inputlength - order)
    current_chars = input_text[random_index:random_index + order]
    text = list(current_chars)
    for _ in range(size - order):
        if current_chars in n_grams_probs:
            next_chars = list(n_grams_probs[current_chars].keys())
            next_chars_weights = list(n_grams_probs[current_chars].values())
            next_char = random.choices(next_chars, next_chars_weights)[0]
            text.append(next_char)
            current_chars = current_chars[1:] + next_char
        else:
            random_index = random.randint(0, inputlength - order)
            next_chars = input_text[random_index:random_index + order]
            text.extend(list(current_chars))

    text = "".join(text[:size])
    with open(outputfile, "w") as f:
        f.write(text)

if __name__ == '__main__':
    inputfile = sys.argv[1]
    input_text = open(inputfile, "r").read()
    size = int(sys.argv[2])
    outputfile = sys.argv[3]

    #Testy na norm_hamlet.txt
    #Generator Markova pierwszego rzedu
    #generator_markova(input_text, size, outputfile, 1)


    #Generator Markova trzeciego rzedu
    #generator_markova(input_text, size, outputfile, 3)

    #Generator Markova piatego rzedu
    #generator_markova(input_text, size, outputfile, 5)

