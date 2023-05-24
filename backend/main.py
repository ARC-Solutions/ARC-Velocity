import json
from flask import Flask, Response, send_from_directory
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import os
from racing import forward_on, foward_off, backward_on, backward_off, right_on, right_off, left_on, left_off
from arduino_Connection import arduino
from ai import start_ai_car

REACT_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../build')

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

@app.route('/racing', methods=['POST'])
def racing_on():
    arduino.write(b'petronas\n')
    print('changing color')
    return Response(json.dumps({'result': 'PetronasColor'}), mimetype='application/json')
@app.route('/ai', methods=['POST'])
def ai_on():
    arduino.write(b'ineos\n')
    start_ai_car(arduino)
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
