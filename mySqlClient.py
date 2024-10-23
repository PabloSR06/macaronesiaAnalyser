import mysql.connector
import os


class MySqlClient:
    def __init__(self):

        self.cursor = None
        self.conn = None

    def get_reader_connection(self):
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER_READER'),
            password=os.getenv('DB_PASSWORD_READER'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME')
        )
    
    def create_connection(self):
        if self.conn is None or not self.conn.is_connected():
            try:
                self.conn = mysql.connector.connect(
                    host=os.getenv('DB_HOST'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    port=os.getenv('DB_PORT')
                )
                self.cursor = self.conn.cursor()
                self.cursor.execute("SHOW DATABASES LIKE %s", (os.getenv('DB_NAME'),))
                result = self.cursor.fetchone()

                if not result:
                
                    with open('schema.sql', 'r') as schema_file:
                        schema_sql = schema_file.read()

                    for statement in schema_sql.split(';'):
                        if statement.strip():
                            self.cursor.execute(statement)
                else:
                    self.conn.database = os.getenv('DB_NAME')

            except mysql.connector.Error as err:
                print(f"Error: No se pudo crear la base de datos: {err}")


    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def get_club_id(self, club_name):
        self.cursor.execute("SELECT id FROM clubs WHERE name = %s", (club_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        
        self.cursor.execute("INSERT INTO clubs (name) VALUES (%s)", (club_name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_archer_id(self, archer_name, club_id):
        self.cursor.execute("SELECT id FROM archers WHERE name = %s AND club_id = %s", (archer_name, club_id))
        result = self.cursor.fetchone()
        if result:
            return result[0]

        self.cursor.execute("INSERT INTO archers (name, club_id) VALUES (%s, %s)", (archer_name, club_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_category_id(self, category_name):
        self.cursor.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        
        self.cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_season_id(self, year, location):
        self.cursor.execute("SELECT id FROM seasons WHERE year = %s AND location = %s", (year, location))
        result = self.cursor.fetchone()
        if result:
            return result[0]

        self.cursor.execute("INSERT INTO seasons (year, location) VALUES (%s, %s)", (year, location))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_round_id(self, season_id, round_number, round_date):
        self.cursor.execute("SELECT id FROM rounds WHERE season_id = %s AND round_number = %s", (season_id, round_number))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        
        self.cursor.execute("INSERT INTO rounds (season_id, round_number, round_date) VALUES (%s, %s, %s)", (season_id, round_number, round_date))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_result(self, round_id, archer_id, category_id, score):
        try:
            self.cursor.execute("INSERT INTO results (round_id, archer_id, category_id, score) VALUES (%s, %s, %s, %s)", (round_id, archer_id, category_id, score))
            self.conn.commit()
        except Exception as e:
            print(f"Error al insertar el resultado: {e}")

    def __del__(self):
        self.close_connection()
