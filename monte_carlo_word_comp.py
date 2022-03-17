# the purpose of this script is to estimate how many
# manual word comparisons would be necessary to
# assign semantic similarity values to all pairs of a
# given word list.  automation rules like
# semantic transitivity (e.g. if A-B = 1 and B-C = 1, A-C = 1)
# aim to reduce the manual comparisons down from (n^2)/2
import itertools
import random

WORD_FILE = "words.txt"
random.seed(10)

def import_wordlist():
    with open(WORD_FILE, "r") as f:
        words = f.read().splitlines()
    return words

def main():
    words = import_wordlist()
    words = words[60:65]
    pairs = list(itertools.combinations(words, 2))
    print(pairs[:4])
    print(type(pairs[3]))
    print(random.randint(0,5))


if __name__ == "__main__":
    main()
