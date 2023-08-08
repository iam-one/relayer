import serial
from flask import Flask, request
from time import sleep

# ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
ser = serial.Serial("/dev/cu.usbmodem21201", 9600, timeout=1)

app = Flask(__name__)

@app.route('/device/state/<int:device>', methods = ['PUT'])
def update(device):
    if request.method == 'PUT':
        state = request.get_json()
        if state == "true":
            ser.write(str.encode("O %d\n"%device))
        else:
            ser.write(str.encode("F %d\n"%device))

    while(True):
        if ser.readable():
            if str(ser.readline()).split("'")[1] == "OK\r": break

    return 'OK'

@app.route('/device/state')
def getState():
    ser.write(str.encode("M\n"))
    while(True):
        if ser.readable():
            buffer = str(ser.readline()).split("'")[1][:-2]
            if len(buffer) == 11: break
    return buffer

if __name__ == '__main__':
    app.run(debug=True, port=9999)