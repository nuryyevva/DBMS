import csv
import codecs
import re
import sqlite3 as sq


def users_filter(file_path, encoding):
    filtered_arr = []
    with codecs.open(file_path, 'r', encoding) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data = row[0]
            parsed_data = parse(data)
            if all(parsed_data):  # eliminate cases where geo or email is not given
                filtered_arr.append(parsed_data)

    # CREATING DATA BASE
    with sq.connect("bets.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS USERS (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        geo TEXT);""")
        cur.executemany("INSERT INTO USERS VALUES(?, ?, ?)", filtered_arr)


def parse(data):
    match = re.match(r'User_(\d+)\t(.*?)\t(.*)', data)
    if match:
        user_id = match.group(1)
        email = match.group(2)
        geo = match.group(3)
        return int(user_id), email, geo
    return None, None, None


if __name__ == "__main__":
    users_filter('users.csv', 'koi8_r')