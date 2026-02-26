import sys
import random
import string
import json
import os

DB_FILE = "urls.json"


def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def main():
    args = sys.argv[1:]
    db = load_db()

    if not args:
        print("Usage: ")
        print(" python3 shorty.py shorten <long-url>")
        print(" python3 shorty.py expand <short-code>")
        return

    command = args[0]

    if command == "shorten":
        long_url = args[1]

        code = generate_short_code()
        while code in db:
            code = generate_short_code()

        db[code] = long_url
        save_db(db)
        print("Short code: ", code)

    elif command == "expand":
        short_code = args[1]
        long_url = db.get(short_code)

        if long_url:
            print("Long URL: ", long_url)
        else:
            print("Not found")

    else:
        print("Unkown command: ", command)


if __name__ == "__main__":
    main()
