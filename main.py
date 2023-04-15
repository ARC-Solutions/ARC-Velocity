import serial
import json
from flask import Flask, Response, send_from_directory
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import os

REACT_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './build')

arduino = serial.Serial('COM3', 9600, timeout=1)

app = Flask(__name__, static_folder='./src', template_folder='./public')
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

executor = ThreadPoolExecutor(max_workers=os.cpu_count())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(REACT_BUILD_DIR, path)):
        return send_from_directory(REACT_BUILD_DIR, path)
    else:
        return send_from_directory(REACT_BUILD_DIR, 'index.html')

def forward_on():
    try:
        print('car go forward')
        arduino.write(b'forward_on\n')
        return Response(json.dumps({'result': 'forward'}), mimetype='application/json')
    except serial.SerialTimeoutException:
        return Response(json.dumps({'error': 'Serial Timeout'}), mimetype='application/json')
def foward_off():
    try:
        print('not forward')
        arduino.write(b'forward_off\n')
        return Response(json.dumps({'result': 'forward_off'}), mimetype='application/json')
    except serial.SerialTimeoutException:
        return Response(json.dumps({'error': 'Serial Timeout'}), mimetype='application/json')

def backward_on():
    try:
        print('car go backwards')
        arduino.write(b'backward_on\n')
        return Response(json.dumps({'result': 'backward'}), mimetype='application/json')
    except serial.SerialTimeoutException:
        return Response(json.dumps({'error': 'Serial Timeout'}), mimetype='application/json')
def backward_off():
    try:
        print('not backwards')
        arduino.write(b'backward_off\n')
        return Response(json.dumps({'result': 'backward_off'}), mimetype='application/json')
    except serial.SerialTimeoutException:
        return Response(json.dumps({'error': 'Serial Timeout'}), mimetype='application/json')


def right_on():
    try:
        print('car go right')
        arduino.write(b'right_on\n')
        return Response(json.dumps({'result': 'right'}), mimetype='application/json')
    except serial.SerialTimeoutException:
        return Response(json.dumps({'error': 'Serial Timeout'}), mimetype='application/json')
def right_off():
    try:
        print('not right')
        arduino.write(b'right_off\n')
        return Response(json.dumps({'result': 'right_off'}), mimetype='application/json')
    except serial.SerialTimeoutException:
        return Response(json.dumps({'error': 'Serial Timeout'}), mimetype='application/json')


def left_on():
    try:
        print('car go left')
        arduino.write(b'left_on\n')
        return Response(json.dumps({'result': 'left'}), mimetype='application/json')
    except serial.SerialTimeoutException:
        return Response(json.dumps({'error': 'Serial Timeout'}), mimetype='application/json')
def left_off():
    try:
        print('not left')
        arduino.write(b'left_off\n')
        return Response(json.dumps({'result': 'left_off'}), mimetype='application/json')
    except serial.SerialTimeoutException:
        return Response(json.dumps({'error': 'Serial Timeout'}), mimetype='application/json')


@app.route('/racing', methods=['POST'])
def racing_on():
    arduino.write(b'petronas\n')
    print('changing color')
    return Response(json.dumps({'result': 'PetronasColor'}), mimetype='application/json')

@app.route('/ai', methods=['POST'])
def ai_on():
    arduino.write(b'ineos\n')
    print('changing color')
    return Response(json.dumps({'result': 'IneosColor'}), mimetype='application/json')

@app.route('/video', methods=['POST'])
def led_off():
    arduino.write(b'led_off\n')
    print('leds turning off')
    return Response(json.dumps({'result': 'LedsOFF'}), mimetype='application/json')

@app.route('/home', methods=['POST'])
def home_on():
    arduino.write(b'home\n')
    print('default color')
    return Response(json.dumps({'result': 'White'}), mimetype='application/json')

@app.route('/forward', methods=['POST'])
def forward():
    return executor.submit(forward_on).result()
@app.route('/forward-off', methods=['POST'])
def forward_off_route():
    return executor.submit(foward_off).result()

@app.route('/backward', methods=['POST'])
def backward():
    return executor.submit(backward_on).result()
@app.route('/backward-off', methods=['POST'])
def backward_off_route():
    return executor.submit(backward_off).result()

@app.route('/right', methods=['POST'])
def right():
    return executor.submit(right_on).result()
@app.route('/right-off', methods=['POST'])
def right_off_route():
    return executor.submit(right_off).result()

@app.route('/left', methods=['POST'])
def left():
    return executor.submit(left_on).result()
@app.route('/left-off', methods=['POST'])
def left_off_route():
    return executor.submit(left_off).result()




if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
