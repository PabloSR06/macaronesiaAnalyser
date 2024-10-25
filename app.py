from flask import Flask, jsonify, request, render_template

from client.azureOpenAIClient import AzureOpenAIClient

from client.mySqlClient import MySqlClient
from recognizer.saveInDatabase import json_to_database # type: ignore


app = Flask(__name__)


@app.route('/api/ask/<question>', methods=['GET', 'POST'])
@app.route('/api/ask', methods=['POST'])
def ask_for_data(question=None):
    if request.method == 'POST':
        data = request.json
        if data and 'question' in data:
            question = data['question']
    
    if question is None:
        return jsonify({'error': 'No question provided'}), 400


    azure_client = AzureOpenAIClient.get_instance()
    response = azure_client.get_response(question)

    if response is None:
        return jsonify({"error": "No se pudo obtener datos"}), 500
    return jsonify({"response": response})

@app.route('/api/process/json', methods=['GET'])
def process_json():
    response = json_to_database()
    if response is None:
        return jsonify({"error": "No se pudo procesar"}), 500
    return jsonify({"response": response})

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health/database', methods=['GET'])
def health_database():
    client = MySqlClient.get_instance()
    response = client.health_check()
    return response


if __name__ == "__main__":
    #app.run(host='0.0.0.0' , debug=True, port=8080)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)