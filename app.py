from flask import Flask, jsonify, request
from json.old.azureOpenAIClient import AzureOpenAIClient

from recognizer.saveInDatabase import json_to_database # type: ignore


app = Flask(__name__)


@app.route('/api/ask/<question>', methods=['GET'])
def ask_for_data(question):
    azure_client = AzureOpenAIClient()
    response = azure_client.gerResponse(question)
    if response is None:
        return jsonify({"error": "No se pudo obtener los puntos del arquero"}), 500
    return jsonify({"response": response})

@app.route('/api/process/json', methods=['GET'])
def process_json():
    response = json_to_database()
    if response is None:
        return jsonify({"error": "No se pudo procesar"}), 500
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
