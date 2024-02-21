"""
Script to import multiple antibodies into the database from a csv file
"""
import psycopg
import os
import csv
import logging
import sys

DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
CSV_FILE = os.path.join(os.path.dirname(__file__), "res","types.csv")

TABLE_NAME = # TODO CHANGEME

logging.basicConfig(level=logging.DEBUG)

def connect():
    logging.info(f"Connecting to {DB_HOST}:{DB_PORT} as {DB_USER} on {DB_NAME} with password {DB_PASSWORD}")

    conn = psycopg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME, port=DB_PORT
    )
    return conn

def test_connection(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    cursor.close()
    assert result[0] == 1
    logging.info("Connection successful")

    sys.exit(0)

def read_csv():
    data = []
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            data.append(row)

    return data

def insert_antibody(conn, row):
    name = f"{row[0]} ({row[1]})"
    producer = row[2]
    article_number = row[3]

    cursor = conn.cursor()
    query = f"INSERT INTO {TABLE_NAME} (name, producer, article_number) VALUES ('{name}', '{producer}', '{article_number}')"
    try:
        cursor.execute(
            query
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()


def main():
    data = read_csv()
    conn = connect()

    # Debugging
    # test_connection(conn)

    for i, row in enumerate(data):
        logging.debug(f"Updating row {i+1}/{len(data)}")

        try:
            insert_antibody(conn, row)
        except Exception as e:
            logging.error(f"Failed to insert antibody {row[0]}")
            logging.error(e)
            continue
    
    conn.close()

if __name__ == "__main__":
    main()