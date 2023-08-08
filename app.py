import serial
from flask import Flask, request, jsonify

# ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
ser = serial.Serial("/dev/tty.usbmodem1101", 9600, timeout=1)

app = Flask(__name__)

@app.route('/device/<device>/state', methods = ['GET','PUT'])
def update(device):
    if request.method == 'PUT':
        buffer = ""
        state = request.get_json()["state"]

        if state == "true":
            ser.write(str.encode("T " + str(device) + "\\n"))
        else:
            ser.write(str.encode("F " + str(device) + "\\n"))

        while(True):
            if ser.readable():
                if str(ser.readline()).split("'")[1][:-2] == "OK\\r": break

        return 'Device %s Updated: %s'%(device, state)

@app.route('/device/state')
def getState():
    buffer = ""
    data = {}
    ser.write(str.encode("M\\n"))
    while(True):
        if ser.readable():
            buffer += str(ser.readline()).split("'")[1][:-2]
            if buffer != "" and str(ser.readline()).split("'")[1][:-2] == "OK\\r": break

    for i in range(len(buffer)):
        if buffer[i] == "T": data[i] = "true"
        else: data[i] = "false"

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=9999)

# Periodically send “P\n” and wait for “OK\n”.→ device health check.