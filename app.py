from flask import Flask, jsonify, request
from azureOpenAIClient import AzureOpenAIClient
from db import get_archer_scores
from recognizer.saveInDatabase import json_to_database # type: ignore


app = Flask(__name__)

@app.route('/api/points/<archer_name>', methods=['GET'])
def get_data(archer_name):
    scores = get_archer_scores(archer_name)
    if scores is None:
        return jsonify({"error": "No se pudo obtener los puntos del arquero"}), 500
    return jsonify(scores)

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
