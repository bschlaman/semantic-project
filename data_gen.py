import psycopg2
import psycopg2.extras
import json
import string
import random
import re
import itertools
from utils import timer

# this decorator keeps a single instance of
# conn and cursor for duration of function call
def conn_cursor(func):
    def wrapper(*args, **kwargs):
        prefix = "[wrapper] "
        print(f"{prefix}Connecting to db... ", end="")
        try:
            conn = psycopg2.connect(**args[0])
        except Exception as err:
            print(f"\nCould not connect to db: {err} (type: {type(err)}")
        else:
            print("Done.")
            # if context exits successfully, transaction is committed
            # if context exits with exception, transaction is rolled back
            with conn, conn.cursor() as cursor:
                try:
                    func(cursor, *args[1:])
                except KeyboardInterrupt:
                    print()
                # TODO: this may be bad practice
                # not clear if a transaction will be rolled back
                # if all exceptions are caught.
                # may want to except all psycopg2.errors differently
                # from more generic ones
                except Exception as err:
                    print(f"error: {err} (type: {type(err)})")
            conn.close()
            print(f"{prefix}Closed connection.")
    return wrapper

@conn_cursor
def test_connection(cursor):
    query = "SELECT CURRENT_TIMESTAMP"
    cursor.execute(query)
    res = cursor.fetchone()[0]
    print(f"{query} -> {res}")

@conn_cursor
def get_table_size(cursor, table_name):
    query = "SELECT pg_size_pretty(pg_total_relation_size(%s))"
    cursor.execute(query, (table_name,))
    res = cursor.fetchone()[0]
    print(f"{query} -> {res}")

@conn_cursor
def insert_word_pair(cursor, word_pair):
    query = (
        f"INSERT INTO words"
        " (updated_at, word1, word2) VALUES"
        " (CURRENT_TIMESTAMP, %s, %s)")
    cursor.execute(query, word_pair)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def import_wordlist():
    with open("words.txt", "r") as f:
        words = f.read().splitlines()
    return words

# for testing purposes
@timer
@conn_cursor
def generate_noise(cursor):
    for _ in range(200):
        words = map(lambda _: "".join(
            random.choices(
            string.ascii_lowercase + string.digits, k=random.randrange(5,7))
            ), [None, None])
        word_pair = tuple(sorted(words))

        query = (
            f"INSERT INTO words"
            " (updated_at, word1, word2) VALUES"
            " (CURRENT_TIMESTAMP, %s, %s)")
        cursor.execute(query, word_pair)

@timer
def generate_pairs(words):
    print("generating pairs...")
    # TODO: dedupe on word.lower
    WORD_BLOCKLIST = ["OK"]
    for w in WORD_BLOCKLIST: words.remove(w)

    words = words[:3707]

    # w1 must come before w2 lexicographically, ignoring special chars
    # below are alternative sort methods which are not compatible
    # with postgres default sorting.  python sorting must be used in
    # conjunction with postgres COLLATE "C" for word columns
    # words.sort(key=lambda s: re.sub('[^A-Za-z]+', "", s).lower())
    # words.sort(key=str.lower)
    words.sort()
    pairs = list(itertools.combinations(words, 2))
    random.shuffle(pairs) # want random word order in db
    return pairs

@timer
@conn_cursor
def upload_pairs(cursor, pairs: list[tuple]):
    # pairs = pairs[:50000]
    print(f"records to insert: {len(pairs)}")
    query = (
        f"INSERT INTO words"
        " (updated_at, word1, word2) VALUES"
        " (CURRENT_TIMESTAMP, %s, %s)")
    psycopg2.extras.execute_batch(cursor, query, pairs, page_size=100000)

def main():
    cfg = load_config()
    words = import_wordlist()

    db_params = cfg["db_connection"]
    test_connection(db_params)
    get_table_size(db_params, "words")
    # generate_noise(db_params)
    # pairs = generate_pairs(words)
    # upload_pairs(db_params, pairs)

if __name__ == "__main__":
    main()
