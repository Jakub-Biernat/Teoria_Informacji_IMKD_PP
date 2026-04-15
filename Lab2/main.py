import random
import sys
from collections import defaultdict

def generator_markova(input_text, size, outputfile, order):
    words = input_text.split()
    inputlength = len(words)

    #Slownik n-gramow, zliczanie ile razy po danym ciagu slow wystepuje inne slowo
    n_grams = defaultdict(lambda: defaultdict(int))
    for i in range(inputlength - order):
        word_set = tuple(words[i : i + order])
        next_word = words[i + order]
        n_grams[word_set][next_word] += 1

    #Rozklad prawdopodobienstwa wystapienia kolejnego slowa dla kazdego n-gramu
    n_grams_probs = {}
    for word_set in n_grams:
        total = sum(n_grams[word_set].values())
        n_grams_probs[word_set] = {
            word: count / total
            for word, count in n_grams[word_set].items()
        }

    #Zaczynamy od losowego ciagu slow wystepujacych w tekscie
    random_index = random.randint(0, inputlength - order)
    current_words = tuple(words[random_index : random_index + order])
    text = list(current_words)
    #Generator
    for _ in range(size - order):
        #Jezeli aktualny ciag istnieje w tekscie ( w slowniku n-gramow)
        if current_words in n_grams_probs:
            #Losowanie nastepnego slowa
            next_words = list(n_grams_probs[current_words].keys())
            next_words_weights = list(n_grams_probs[current_words].values())
            next_word = random.choices(next_words, next_words_weights)[0]
            text.append(next_word)
            #Aktualizacja aktualnego ciagu
            current_words = tuple(list(current_words[1 :]) + [next_word])
        #Jezeli w tekscie nie istnial aktualny ciag, losuje nowy z tekstu
        else:
            random_index = random.randint(0, inputlength - order)
            current_words = tuple(words[random_index : random_index + order])
            text.extend(list(current_words))

    #Zapis do pliku wyjsciowego
    text = " ".join(text[:size])
    with open(outputfile, "w") as f:
        f.write(text)

if __name__ == '__main__':
    inputfile = sys.argv[1]
    input_text = open(inputfile, "r").read()
    size = int(sys.argv[2])
    outputfile = sys.argv[3]

    #Generator Markova pierwszego rzedu
    #generator_markova(input_text, size, outputfile, 1)

    #Generator Markova drugiego rzedu
    #generator_markova(input_text, size, outputfile, 2)

    #Generator Markova drugiego rzedu, input zaczyna sie na probability
    input_text = "probability " + input_text
    generator_markova(input_text, size, outputfile, 2)

