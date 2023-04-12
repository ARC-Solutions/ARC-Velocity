import serial
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import os

REACT_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './build')

arduino = serial.Serial('COM3', 9600)

app = Flask(__name__, static_folder='./src', template_folder='./public')
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

executor = ThreadPoolExecutor(max_workers=7)
f1 = executor.submit(app.route, '/home')
f2 = executor.submit(app.route, '/forward')
f3 = executor.submit(app.route, '/backward')
f4 = executor.submit(app.route, '/right')
f5 = executor.submit(app.route, '/left')
f1.result()
f2.result()
f3.result()
f4.result()
f5.result()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(REACT_BUILD_DIR, path)):
        return send_from_directory(REACT_BUILD_DIR, path)
    else:
        return send_from_directory(REACT_BUILD_DIR, 'index.html')

@app.route('/forward', methods=['POST'])
def forward():
    try:
        print('car go forward')
        arduino.write(b'forward_on\n')
        return jsonify({'result': 'forward'})
    except serial.SerialTimeoutException:
        return jsonify({'error': 'Serial Timeout'})
@app.route('/forward-off', methods=['POST'])
def foward_off():
    try:
        print('not forward')
        arduino.write(b'forward_off\n')
        return jsonify({'result': 'forward_off'})
    except serial.SerialTimeoutException:
        return jsonify({'error': 'Serial Timeout'})

@app.route('/right', methods=['POST'])
def right():
    try:
        print('car go right')
        arduino.write(b'right_on')
        return jsonify({'result': 'right'})
    except serial.SerialTimeoutException:
        return jsonify({'error': 'Serial Timeout'})

@app.route('/right-off', methods=['POST'])
def right_off():
    try:
        print('not right')
        arduino.write(b'right_off')
        return jsonify({'result': 'right-off'})
    except serial.SerialTimeoutException:
        return jsonify({'error': 'Serial Timeout'})


@app.route('/left', methods=['POST'])
def left():
    try:
        print('car go left')
        arduino.write(b'left_on')
        return jsonify({'result': 'left'})
    except serial.SerialTimeoutException:
        return jsonify({'error': 'Serial Timeout'})

@app.route('/backward', methods=['POST'])
def backward():
    try:
        print('car go backwards')
        arduino.write(b'backwards_on')
        return jsonify({'result': 'backward'})
    except serial.SerialTimeoutException:
        return jsonify({'error': 'Serial Timeout'})

@app.route('/racing', methods=['POST'])
def racing():
    arduino.write(b'petronas\n')
    print('changing color')
    return jsonify({'result': 'racing'})

@app.route('/ai', methods=['POST'])
def ai():
    arduino.write(b'ineos\n')
    print('changing color')
    return jsonify({'result': 'ai'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
