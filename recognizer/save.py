import json
import datetime
import sys
from mySqlClient import MySqlClient

def process_json(json_path, default_location, default_year):
    
    result = None

    with open(json_path, 'r', encoding='utf-8') as f:
        result = json.load(f)

    filename = json_path.split('/')[-1]

    mysql_client = MySqlClient()
    mysql_client.create_connection()
    for idx, document in enumerate(result.get('analyzeResult', {}).get('documents', [])):
        
        fields = document.get('fields', {})
        year = fields.get('year', {}).get('valueString', default_year)
        year = year.split('-')[0].strip()

        location = fields.get('location', {}).get('valueString', default_location)
        points = fields.get('points', {})

        season_id = mysql_client.get_season_id(year, location)

        for i, element in enumerate(points.get('valueArray', []), start=1):
            line = element.get('valueObject', {})
            archer_name = line.get('Deportista', {}).get('valueString', "")
            club_name = line.get('Club', {}).get('valueString', "")
            category_name = line.get('División', {}).get('valueString', "")
            
            club_id = mysql_client.get_club_id(club_name)
            archer_id = mysql_client.get_archer_id(archer_name, club_id)
            category_id = mysql_client.get_category_id(category_name)

            for i in range(1, 7):
                key = str(i)
                if key in line:
                    score = line[key]['valueString']
                    if(score == "" or score == "0"):
                        break
                    round_id = mysql_client.get_round_id(season_id, i, datetime.date.today()) 
                    if(round_id == 1 and archer_id == 45 and filename == '2021-2022-2.json'):
                        print("SKIP")
                        break
                    mysql_client.insert_result(round_id, archer_id, category_id, score)

    mysql_client.close_connection()
    print("-----------------------------------")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python save.py <ruta_del_json>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    location = sys.argv[2]
    year = sys.argv[3]
    process_json(json_path, location, year)
