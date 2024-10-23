import json
import os
import re
from dotenv import load_dotenv
from openai import AzureOpenAI

from mySqlClient import MySqlClient


load_dotenv()

class AzureOpenAIClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AzureOpenAIClient, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'): 
            self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
            self.model = os.getenv("AZURE_OPENAI_MODEL")
            self.key = os.getenv("AZURE_OPENAI_KEY")
            self.api_version = os.getenv("AZURE_OPENAI_VERSION")

            self.client = AzureOpenAI(azure_endpoint=self.endpoint, api_key=self.key, api_version=self.api_version)
            
            self.sql_client = MySqlClient.get_instance()

            self.sql_script = """
    -- Clubs Table
    CREATE TABLE IF NOT EXISTS clubs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL UNIQUE
    );

    -- Archers Table
    CREATE TABLE IF NOT EXISTS archers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        club_id INT NOT NULL,
        FOREIGN KEY (club_id) REFERENCES clubs(id),
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Categories Table
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );

    -- Seasons Table
    CREATE TABLE IF NOT EXISTS seasons (
        id INT AUTO_INCREMENT PRIMARY KEY,
        year YEAR NOT NULL,
        location VARCHAR(50) NOT NULL,
        UNIQUE (year, location)
    );

    -- Rounds Table
    CREATE TABLE IF NOT EXISTS rounds  (
        id INT AUTO_INCREMENT PRIMARY KEY,
        season_id INT NOT NULL,
        round_number INT NOT NULL,
        round_date DATE NULL,
        FOREIGN KEY (season_id) REFERENCES seasons(id),
        UNIQUE (season_id, round_number)
    );

    -- Round Results Table
    CREATE TABLE IF NOT EXISTS results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        round_id INT NOT NULL,
        archer_id INT NOT NULL,
        category_id INT NOT NULL,
        score INT NOT NULL,
        FOREIGN KEY (round_id) REFERENCES rounds(id),
        FOREIGN KEY (archer_id) REFERENCES archers(id),
        FOREIGN KEY (category_id) REFERENCES categories(id),
        UNIQUE (round_id, archer_id, category_id)
    );
    """

            self.json_example = '{"query": "SQL_QUERY_HERE"}'
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AzureOpenAIClient()
        return cls._instance
    
    def generate_queries(self, user_message):
        messages = [
            {
                "role": "system",
                "content": f"Teniendo en cuenta el esquema de la base de datos MYSQL, convierte la consulta en lenguaje natural a una consulta SQL que maneje coincidencias parciales en nombres y proporciona solo la consulta SQL en formato JSON. La consulta debe devolver los datos solicitados basándose en los nombres proporcionados por el usuario. Aquí está el esquema de la base de datos: {self.sql_script} La consulta SQL debe buscar todos los nombres que contengan la subcadena especificada por el usuario. Por ejemplo, si el usuario solicita información sobre 'pepe', la consulta debe utilizar LIKE '%pepe%' para manejar coincidencias parciales. No puedes eliminar, actualiazar o crear datos. Proporciona la salida solo en el siguiente formato JSON: {self.json_example}"
            },
            {
                "role": "user",
                "content": "La pregunta es: " + user_message
            },
        ]
        completion = self.client.chat.completions.create(  
        model=self.deployment,  
        messages=messages,  
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False  
      )
        return completion.to_json()
    
    def generate_response(self, user_message, data):
        messages = [
            {
                "role": "system",
                "content": f"Usa los datos proporcionados para responder dinámicamente a las preguntas del usuario. Tu tarea es procesar estos datos y proporcionar una respuesta clara y precisa según la pregunta del usuario."
            },
            {
                "role": "user",
                "content": "La pregunta es: " + user_message  + " y los datos son: " + str(data)
            },
        ]
        completion = self.client.chat.completions.create(  
        model=self.deployment,  
        messages=messages,  
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False  
      )
        return completion.to_json()
    
    def prepare_query(self, json_response):
        query=None
        try:
            data = json.loads(json_response).get('choices', [])[0].get('message', {}).get('content', '')
            cleaned_str = re.sub(r'```\w*\n|\n```', '', data).strip("'")
            query = json.loads(cleaned_str)
        except (IndexError, KeyError, json.JSONDecodeError) as e:
            print(f"Error processing JSON response: {e}")
            json_data = {}
        return query
    
    def prepare_response(self, json_response):
        try:
            data = json.loads(json_response).get('choices', [])[0].get('message', {}).get('content', '')

        except (IndexError, KeyError, json.JSONDecodeError) as e:
            print(f"Error processing JSON response: {e}")
            json_data = {}
        return data
    
    def execute_queries(self, query):
        conn = None
        cursor = None
        try:
            conn = self.sql_client.get_reader_connection()
            cursor = conn.cursor()
           
            print(f"Executing query: {query.get('query')}")
            cursor.execute(query.get('query'))
            results = cursor.fetchall()
            conn.commit()
        except Exception as err:
            print(f"Error: {err}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return results

    def get_response(self, text):
        query_json = self.generate_queries(text)
        query = self.prepare_query(query_json)
        data = self.execute_queries(query)
        response_json = self.generate_response(text, data)
        response = self.prepare_response(response_json)
        return response



