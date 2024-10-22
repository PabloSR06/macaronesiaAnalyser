import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

def create_database(cursor):
    try:
        cursor.execute(
            f"CREATE DATABASE {os.getenv('DB_NAME')} DEFAULT CHARACTER SET 'utf8'"
        )
    except mysql.connector.Error as err:
        print(f"Error: No se pudo crear la base de datos: {err}")
        exit(1)

def create_tables(cursor):
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()
    for statement in schema_sql.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.Error as err:
                print(f"Error: {err.msg}")

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME')
        )
    except mysql.connector.Error as err:
        print(err)
        return None
    return conn

def get_archer_scores(archer_name):
    conn = get_db_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT results.score, rounds.round_date
            FROM results
            JOIN archers ON results.archer_id = archers.id
            JOIN rounds ON results.round_id = rounds.id
            WHERE archers.name = %s
        """, (archer_name,))
        scores = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        scores = None
    finally:
        cursor.close()
        conn.close()

    return scores