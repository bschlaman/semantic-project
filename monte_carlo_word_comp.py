# the purpose of this script is to estimate how many
# manual word comparisons would be necessary to
# assign semantic similarity values to all pairs of a
# given word list.  automation rules like
# semantic transitivity (e.g. if A-B = 1 and B-C = 1, A-C = 1)
# aim to reduce the manual comparisons down from (n^2)/2
import itertools
import random
from pprint import pprint

WORD_FILE = "words.txt"
random.seed(9)

# semantic values; sd[(w1, w2)] = 0 - 4
sd = {}

def import_wordlist():
    with open(WORD_FILE, "r") as f:
        words = f.read().splitlines()
    return words

def assign_random_val():
    return random.randrange(0,5)

def apply_rule(w1, w2):
    # A-C is 0 if A-B is 4 and B-C is 0
    for pair in sd:
        if w1 not in pair and w2 not in pair:
            continue
        (sdw1, sdw2) = pair
        if w1 == sdw1:
            pass
    return -1

def main():
    words = import_wordlist()
    random.shuffle(words)
    words = words[:7]
    pairs = list(itertools.combinations(words, 2))
    print(words, len(words))

    manual_comp_count = 0
    for (w1, w2) in pairs:
        res = apply_rule(w1, w2)
        if res == -1:
            manual_comp_count += 1
            res = assign_random_val()
        sd[(w1, w2)] = res
    pprint(sd)
    k = list(sd.keys())
    random.shuffle(k)
    for w in [" ".join(i) for i in k]:
        print(w)
    print(f"manual comparisons: {manual_comp_count}")


if __name__ == "__main__":
    main()
