import random
import sys
from collections import defaultdict

def entropia(input_texts, order):
    for input_text in input_texts:
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
    input_text = "probability " + input_text
    generator_markova(input_text, size, outputfile, 5)
    # Srednia dlugosc slowa: 4.11

