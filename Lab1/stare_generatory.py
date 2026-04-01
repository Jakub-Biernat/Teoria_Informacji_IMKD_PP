def generator_markova_pierwszego_rzedu(input_text, size, outputfile):
    chars = defaultdict(int)
    for char in input_text:
        chars[char] += 1

    inputlength = len(input_text)
    probs = {char: total / inputlength for char, total in chars.items()}

    bigrams = defaultdict(lambda: defaultdict(int))
    for i in range(inputlength - 1):
        bigrams[input_text[i]][input_text[i + 1]] += 1

    bigram_probs = {}
    for first_char in bigrams:
        total = sum(bigrams[first_char].values())
        bigram_probs[first_char] = {
            second_char: count / total for second_char, count in bigrams[first_char].items()
        }

    keys = list(probs.keys())
    weights = list(probs.values())
    current_char = random.choices(keys, weights)[0]
    text = [current_char]
    for _ in range(size - 1):
        if current_char in bigram_probs:
            next_chars = list(bigram_probs[current_char].keys())
            next_chars_weights = list(bigram_probs[current_char].values())
            current_char = random.choices(next_chars, next_chars_weights)[0]
        else:
            current_char = random.choices(keys, weights)[0]
        text.append(current_char)

    text = "".join(text)
    with open(outputfile, "w") as f:
        f.write(text)

def generator_markova_trzeciego_rzedu(input_text, size, outputfile):
    chars = defaultdict(int)
    for char in input_text:
        chars[char] += 1

    inputlength = len(input_text)
    probs = {char: total / inputlength for char, total in chars.items()}

    quadrigrams = defaultdict(lambda: defaultdict(int))
    for i in range(inputlength - 3):
        quadrigrams[input_text[i:i+3]][input_text[i + 3]] += 1

    quadrigram_probs = {}
    for first_three_chars in quadrigrams:
        total = sum(quadrigrams[first_three_chars].values())
        quadrigram_probs[first_three_chars] = {
            next_char: count / total
            for next_char, count in quadrigrams[first_three_chars].items()
        }

    keys = list(probs.keys())
    weights = list(probs.values())
    current_chars = "".join(random.choices(keys, weights, k=3))
    text = list(current_chars)
    for _ in range(size - 3):
        if current_chars in quadrigram_probs:
            next_chars = list(quadrigram_probs[current_chars].keys())
            next_chars_weights = list(quadrigram_probs[current_chars].values())
            next_char = random.choices(next_chars, next_chars_weights)[0]
        else:
            next_char = random.choices(keys, weights)[0]
        text.append(next_char)
        current_chars = current_chars[1:] + next_char

    text = "".join(text[:size])
    with open(outputfile, "w") as f:
        f.write(text)