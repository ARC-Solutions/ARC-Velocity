import time

import serial
arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

