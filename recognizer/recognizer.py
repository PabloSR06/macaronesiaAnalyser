from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import sys
import json
import os



def process_pdf(pdf_path):

    endpoint = os.getenv('RecognizerEndpoint')
    key = os.getenv('RecognizerKey')

    model_id = os.getenv('RecognizerModelId')

    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    result = None


    print(f"Calling the API, please wait...")
    with open(pdf_path, "rb") as f:
        poller = client.begin_analyze_document(model_id, document=f)
        result = poller.result()

    json_folder = 'recognizer/json'
    os.makedirs(json_folder, exist_ok=True)
    json_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '.json'
    json_path = os.path.join(json_folder, json_filename)
    
    # Object of type AnalyzeResult is not JSON serializable
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)
    
    print(f"Result saved to {json_path}")

    print("-----------------------------------")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python recognizer.py <ruta_del_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    process_pdf(pdf_path)
