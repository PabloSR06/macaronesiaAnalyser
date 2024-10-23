import os
import subprocess
import shutil

def json_to_database():
    pdf_directory = 'recognizer/json/'
    old_directory = 'recognizer/json/old/'
    contador = 1

    if not os.path.exists(old_directory):
        os.makedirs(old_directory)

    for filename in os.listdir(pdf_directory):
        if filename.endswith('.json'):
            pdf_path = os.path.join(pdf_directory, filename)

            location = 'SALA'
            year = filename.split('-')[0].strip()

            print(f"Procesando archivo {contador}: {filename}")

            subprocess.run(['c:/dev/macaronesiaAnalyser/.conda/python.exe', 'recognizer/processJson.py', pdf_path, location, year])

            # shutil.move(pdf_path, os.path.join(old_directory, filename))

            contador += 1

    print(f"FINISHED: {contador - 1} archivos procesados")
    return f"FINISHED: {contador - 1} archivos procesados"
