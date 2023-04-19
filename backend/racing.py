import serial
from flask import Response, json
from arduino_Connection import arduino


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

