import random
import sys
from collections import defaultdict

def generator_markova(input_text, size, outputfile, order):
    inputlength = len(input_text)

    #Slownik n-gramow, zliczanie ile razy po danym ciagu znakow wystepuje inny znak
    n_grams = defaultdict(lambda: defaultdict(int))
    for i in range(inputlength - order):
        n_grams[input_text[i : i + order]][input_text[i + order]] += 1

    #Rozklad prawdopodobienstwa wystapienia kolejnego znaku dla kazdego n-gramu
    n_grams_probs = {}
    for first_chars in n_grams:
        total = sum(n_grams[first_chars].values())
        n_grams_probs[first_chars] = {
            next_char: count / total
            for next_char, count in n_grams[first_chars].items()
        }

    #Zaczynamy od losowego ciagu znakow wystepujacego w tekscie
    random_index = random.randint(0, inputlength - order)
    current_chars = input_text[random_index : random_index + order]
    text = list(current_chars)
    #Generator
    for _ in range(size - order):
        #Jezeli aktualny ciag istnieje w tekscie ( w slowniku n-gramow)
        if current_chars in n_grams_probs:
            #Losowanie nastepnego znaku
            next_chars = list(n_grams_probs[current_chars].keys())
            next_chars_weights = list(n_grams_probs[current_chars].values())
            next_char = random.choices(next_chars, next_chars_weights)[0]
            text.append(next_char)
            #Aktualizacja aktualnego ciagu
            current_chars = current_chars[1 :] + next_char
        #Jezeli w tekscie nie istnial aktualny ciag, losuje nowy z tekstu
        else:
            random_index = random.randint(0, inputlength - order)
            current_chars = input_text[random_index: random_index + order]
            text.extend(list(current_chars))

    #Zapis do pliku wyjsciowego
    text = "".join(text[:size])
    with open(outputfile, "w") as f:
        f.write(text)

if __name__ == '__main__':
    inputfile = sys.argv[1]
    input_text = open(inputfile, "r").read()
    size = int(sys.argv[2])
    outputfile = sys.argv[3]

    #Testy na norm_hamlet.txt, dlugosc tekstu wyjsciowego 1000 znakow
    #Srednia dlugosc slowa: 3.98

    #Generator Markova pierwszego rzedu
    #generator_markova(input_text, size, outputfile, 1)
    #Srednia dlugosc slowa: 3.98


    #Generator Markova trzeciego rzedu
    #generator_markova(input_text, size, outputfile, 3)
    # Srednia dlugosc slowa: 4.11

    #Generator Markova piatego rzedu
    generator_markova(input_text, size, outputfile, 5)
    # Srednia dlugosc slowa: 4.11

