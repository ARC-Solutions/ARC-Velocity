import serial
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import os

REACT_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './build')

app = Flask(__name__, static_folder='./src', template_folder='./public')
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

executor = ThreadPoolExecutor(max_workers=1)
f1 = executor.submit(app.route, '/home')
f1.result()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path == "":
        return send_from_directory(REACT_BUILD_DIR, 'index.html')
    else:
        return send_from_directory(REACT_BUILD_DIR, path)

@app.route('/forward', methods=['POST'])
def forward():
    try:
        print('car go forward')
        return jsonify({'result': 'forward'})
    except serial.SerialTimeoutException:
        return jsonify({'error': 'Serial Timeout'})

@app.route('/backward', methods=['POST'])
def backward():
    try:
        print('car go backwards')
        return jsonify({'error': 'backward'})
    except serial.SerialTimeoutException:
        return jsonify({'error': 'Serial Timeout'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
