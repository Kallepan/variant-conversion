import psycopg
import os
import logging
import csv
import sys
logging.basicConfig(level=logging.INFO)

DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
CSV_FILE = os.path.join(os.path.dirname(__file__), "res","convert.csv")
TABLE_NAME = "variants_db_variant"


def connect():
    logging.info(f"Connecting to {DB_HOST}:{DB_PORT} as {DB_USER} on {DB_NAME} with password {DB_PASSWORD}")

    conn = psycopg.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME, port=DB_PORT
    )
    return conn

def read_csv():
    data = []
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            data.append(row)

    return data

def update_variant(conn, row):
    variant_id = row[0]
    variant_new_accession_number = row[6]
    variant_new_genomic_change = row[7]

    cursor = conn.cursor()
    # I know sql injection blah blah, but this is a one time script
    query = f"UPDATE {TABLE_NAME} SET accession_number = '{variant_new_accession_number}', genomic_change = '{variant_new_genomic_change}' WHERE id = {variant_id}"
    
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

def test_connection(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    cursor.close()
    assert result[0] == 1
    logging.info("Connection successful")

    sys.exit(0)

def main():
    data = read_csv()
    conn = connect()

    # Debugging
    # test_connection(conn)

    data.pop(0)  # remove header
    for i, row in enumerate(data):
        logging.debug(f"Updating variant {i+1}/{len(data)}. ID: {row[0]}")
        try:
            update_variant(conn, row)
        except Exception as e:
            logging.error(f"hg38: ({row[1]}, {row[2]}, {row[3]}). hg37: ({row[1]}, {row[6]}, {row[7]}).")
            logging.debug(f"Error: {e}")
            continue
    
    conn.close()



if __name__ == "__main__":
    main()
