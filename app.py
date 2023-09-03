import serial
import schedule
from flask import Flask, request, jsonify
from time import sleep

port = "/dev/ttyUSB0"
port = "/dev/tty.usbmodem1101"
ser = serial.Serial("/dev/tty.usbmodem1101", 9600, timeout=1)

def checkHealth():
    ser.write(str.encode("P\\n"))
    while(True):
        if ser.readable():
            if str(ser.readline()).split("'")[1][:-2] == "OK\\r": break
    print("Device is OK")

schedule.every(5).seconds.do(checkHealth)

app = Flask(__name__)

@app.route('/device/<device>/state', methods = ['PUT'])
def updateState(device):
    if request.method == 'PUT':
        state = request.get_json()["state"]

        if state == "true":
            ser.write(str.encode("T " + str(device) + "\\n"))
        else:
            ser.write(str.encode("F " + str(device) + "\\n"))

        while(True):
            if ser.readable():
                if str(ser.readline()).split("'")[1][:-2] == "OK\\r": break

        return 'Device %s Updated: %s'%(device, state)

@app.route('/device/state', methods = ['GET'])
def getState():
    if request.method == 'GET':
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
    while True:
        schedule.run_pending()
        sleep(1)