import os
import PyPDF2
import mysql.connector

PDF_FILE = 'Clasificación FINAL Liga Macaronesia Sala_2024-2023.pdf'

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        return text

def parse_text(text):
    lines = text.split('\n')
    parsed_data = {'clubs': set(), 'archers': [], 'categories': set(), 'results': []}
    
    category_map = {
        'Arco Recurvo': 'Arco Recurvo',
        'Arco Compuesto': 'Arco Compuesto',
        'Arco Desnudo': 'Arco Desnudo',
        'Arco Tradicional': 'Arco Tradicional',
        'Arco Longbow': 'Arco Longbow',
        'Precisión': 'Precisión'
    }

    current_category = None
    for line in lines:
        for key in category_map:
            if key in line:
                current_category = category_map[key]
                parsed_data['categories'].add(current_category)
                break
        if any(char.isdigit() for char in line):
            parts = line.split()
            name = ' '.join(parts[1:-2])
            club = parts[-2]
            try:
                score = int(parts[-1])
            except ValueError:
                continue  # Skip this line if the score is not a valid integer
            parsed_data['clubs'].add(club)
            parsed_data['archers'].append((name, club))
            parsed_data['results'].append((name, club, current_category, score))
    
    return parsed_data

def initialize_database(parsed_data):
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME')
    )
    cursor = conn.cursor()


    for club in parsed_data['clubs']:
        cursor.execute('INSERT IGNORE INTO clubs (name) VALUES (%s)', (club,))
    
    for category in parsed_data['categories']:
        cursor.execute('INSERT IGNORE INTO categories (name) VALUES (%s)', (category,))

    conn.commit()

    for archer in parsed_data['archers']:
        name, club = archer
        cursor.execute('SELECT id FROM clubs WHERE name=%s', (club,))
        club_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO archers (name, club_id) VALUES (%s, %s)', (name, club_id))

    conn.commit()

    for result in parsed_data['results']:
        name, club, category, score = result
        cursor.execute('SELECT id FROM archers WHERE name=%s AND club_id=(SELECT id FROM clubs WHERE name=%s)', (name, club))
        archer_id = cursor.fetchone()[0]
        cursor.execute('SELECT id FROM categories WHERE name=%s', (category,))
        category_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO results (archer_id, category_id, score, round_id) VALUES (%s, %s, %s, %s)', (archer_id, category_id, score, 1))  # Added round_id value

    conn.commit()
    conn.close()

if __name__ == '__main__':
    extracted_text = extract_text_from_pdf(PDF_FILE)
    parsed_data = parse_text(extracted_text)
    initialize_database(parsed_data)