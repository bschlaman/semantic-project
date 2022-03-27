import psycopg2
import time
import json

# used to time individual functions
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print(f" - time: {(time.perf_counter() - start):.3f}")
        return res
    return wrapper

# keeps a single instance of conn and cursor for duration of function call
# might want to move to contextmanager in the future
def conn_cursor(func):
    def wrapper(*args, **kwargs):
        prefix = "[wrapper] "
        print(f"{prefix}Connecting to db... ", end="")
        try:
            conn = psycopg2.connect(**args[0])
        except Exception as err:
            print(f"\nCould not connect to db: {err}")
        else:
            cursor = conn.cursor()
            print("Done.")
            try:
                func(conn, cursor, *args[1:])
            except KeyboardInterrupt:
                print()
            print(f"{prefix}Committing conn...")
            conn.commit()
            cursor.close()
            conn.close()
    return wrapper

@conn_cursor
def test_connection(conn, cursor):
    query = "SELECT CURRENT_TIMESTAMP"
    cursor.execute(query)
    res = cursor.fetchone()[0]
    print(f"{query} -> {res}")

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def main():
    cfg = load_config()
    db_params = cfg["db_connection"]
    test_connection(db_params)

if __name__ == "__main__":
    main()
