import csv
import codecs
import re
import sqlite3 as sq


def log_filter(file_path, encoding):
    filtered_arr = []
    with codecs.open(file_path, "r", encoding) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            filtered_data = extract(row)
            if all(filtered_data[:2]):  # eliminate cases where there are no date
                filtered_arr.append(filtered_data)

    with sq.connect("bets.db") as con:
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS LOG (
                           user_id INTEGER,
                           time DATETIME,
                           bet REAL,
                           win REAL
                        );"""
        )
        cur.executemany("INSERT INTO LOG VALUES(?, ?, ?, ?)", filtered_arr)


def extract(data):
    user_id_ = re.search(r"user_(\d+)", data[0])
    user_id = user_id_.group(1) if user_id_ else None
    data_time = data[1][1:] if len(data) > 1 and len(data[1]) > 1 else None
    if data_time and len(data_time) != 19:
        data_time = data_time[:11] + "0" + data_time[11:]
    bet = data[2] if len(data) > 2 else None
    win = data[3] if len(data) > 3 else None
    return user_id, data_time, bet, win


if __name__ == "__main__":
    log_filter("log.csv", "utf-8")
