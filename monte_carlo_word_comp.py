# the purpose of this script is to estimate how many
# manual word comparisons would be necessary to
# assign semantic similarity values to all pairs of a
# given word list.  automation rules like
# semantic transitivity (e.g. if A-B = 1 and B-C = 1, A-C = 1)
# aim to reduce the manual comparisons down from (n^2)/2
import itertools
import collections
import random
from pprint import pprint

WORD_FILE = "words.txt"
random.seed(9)

# semantic values; sd[(w1, w2)] = 0 - 4
sd = {}
sem_graph = collections.defaultdict(list)

def import_wordlist():
    with open(WORD_FILE, "r") as f:
        words = f.read().splitlines()
    return words

def assign_random_val():
    return random.randrange(0,5)

def apply_rule(w1, w2):
    # A-C is 0 if there exists B s.t. A-B is 4 and B-C is 0
    # A-C is 0 if there exists B s.t. A-B is 0 and B-C is 4
    for B, sval in sem_graph[w1]:
        if B not in sem_graph: continue
        if sval == 4 and (w2, 0) in sem_graph[B]:
            return 0
        if sval == 0 and (w2, 4) in sem_graph[B]:
            return 0
    return -1

def main():
    words = import_wordlist()
    random.shuffle(words)
    words = words[:111]
    # w1 must come before w2 lexicographically
    words.sort()
    pairs = list(itertools.combinations(words, 2))
    # if pairs are sorted, B will never be found in sem_graph
    random.shuffle(pairs)

    manual_comp_count = 0
    for (w1, w2) in pairs:
        res = apply_rule(w1, w2)
        if res == -1:
            manual_comp_count += 1
            res = assign_random_val()
        sem_graph[w1].append((w2, res))

    print(f"number of words:    {len(words)}")
    print(f"number of pairs:    {len(pairs)}")
    print(f"manual comparisons: {manual_comp_count}")
    print(f"total comparisons:  {len(pairs)}")


if __name__ == "__main__":
    main()
