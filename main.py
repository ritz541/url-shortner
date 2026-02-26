import sys
import random
import string
import sqlite3

DB_FILE = "urls.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    long_url TEXT NOT NULL
    )
""")
    conn.commit()
    conn.close()

def generate_short_code(length:int = 6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

def save_url(short_code: str, long_url: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO urls (short_code, long_url) VALUES (?, ?)", (short_code, long_url)
    )
    conn.commit()
    conn.close()

def get_url(short_code: str):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT long_url FROM urls WHERE short_code = ?", (short_code,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def main():
    init_db()
    args = sys.argv[1:]

    if not args:
        print("Usage: ")
        print(" python3 main.py shorten <long_url>")
        print(" python3 main.py expand <short_code>")
        return
    
    command = args[0]

    if command == "shorten":
        long_url = args[1]

        code = generate_short_code()
        save_url(code, long_url)

        print("Short code: ", code)

    elif command == "expand":
        short_code = args[1]
        long_url = get_url(short_code)

        if long_url:
            print("Long URL: ", long_url)
        else: 
            print("Not found!")

    else:
        print("Unknown command: ", command)

if __name__ == "__main__":
    main()