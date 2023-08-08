import serial
from flask import Flask, request, jsonify
from time import sleep

# ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
ser = serial.Serial("/dev/cu.usbmodem21201", 9600, timeout=1)

app = Flask(__name__)

@app.route('/device/<int:device>/state', methods = ['PUT'])
def update(device):
    if request.method == 'PUT':
        state = request.get_json()["state"]
        if state == "true":
            ser.write(str.encode("O %d\n"%device))
        else:
            ser.write(str.encode("F %d\n"%device))

        while(True):
            if ser.readable():
                if str(ser.readline()).split("'")[1] == "OK\r": break

        return 'Updated: ' + state

@app.route('/device/state')
def getState():
    data = {}
    ser.write(str.encode("M\n"))
    while(True):
        if ser.readable():
            buffer = str(ser.readline()).split("'")[1][:-2]
            if buffer != "" and "OK\\r" not in buffer: break

    for i in range(len(buffer)):
        if buffer[i] == "T": data[i] = "true"
        else: data[i] = "false"

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=9999)