import psycopg2
import time
import json
import string
import random

# used to time individual functions
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print(f" - time: {(time.perf_counter() - start):.3f}")
        return res
    return wrapper

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
def insert_word_pair(cursor, word_pair):
    query = (
        f"INSERT INTO words"
        " (updated_at, word1, word2) VALUES"
        " (CURRENT_TIMESTAMP, %s, %s)")
    cursor.execute(query, word_pair)

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

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

def main():
    cfg = load_config()
    db_params = cfg["db_connection"]
    test_connection(db_params)
    generate_noise(db_params)

if __name__ == "__main__":
    main()
