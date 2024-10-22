import os
import subprocess
import shutil

pdf_directory = 'recognizer/pdf/'
old_directory = 'recognizer/pdf/oldpdf/'
contador = 1

if not os.path.exists(old_directory):
    os.makedirs(old_directory)

for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)

        print(f"Procesando archivo {contador}: {filename}")

        subprocess.run(['c:/dev/macaronesiaAnalyser/.conda/python.exe', 'recognizer/recognizer.py', pdf_path])

        shutil.move(pdf_path, os.path.join(old_directory, filename))

        contador += 1

print(f"FINISHED: {contador - 1} archivos procesados")
