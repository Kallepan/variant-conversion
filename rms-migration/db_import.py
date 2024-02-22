"""
Script to import multiple antibodies into the database from a csv file
"""

import os
import csv
import logging
import sys
import uuid

DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
CSV_FILE = os.path.join(os.path.dirname(__file__), "res", "types.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "queries.sql")

TABLE_NAME = "bak.type"
logging.basicConfig(level=logging.DEBUG)


def read_csv():
    data = []
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            data.append(row)

    data.pop(0)  # Remove header

    return data


def insert_antibody(row):
    name = f"{row[0]} ({row[1]})"
    producer = row[2]
    article_number = row[3]
    id = str(uuid.uuid4())

    return f"INSERT INTO {TABLE_NAME} (id, name, producer, article_number, created_at) VALUES ('{id}', '{name}', '{producer}', '{article_number}', NOW());"


def main():
    if os.path.exists(OUTPUT_FILE):
        logging.info(f"Removing old file {OUTPUT_FILE}")
        os.remove(OUTPUT_FILE)

    data = read_csv()

    # Debugging
    # test_connection(conn)

    queries = []
    for i, row in enumerate(data):
        logging.debug(f"Updating row {i+1}/{len(data)}")

        query = insert_antibody(row)

        queries.append(query)

    with open(OUTPUT_FILE, "w") as file:
        file.write("\n".join(queries))


if __name__ == "__main__":
    main()
