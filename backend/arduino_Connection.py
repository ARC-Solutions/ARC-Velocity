import serial

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

