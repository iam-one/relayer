import serial

port = "/dev/tty.usbmodem1101"
device = 1
buffer = ""

ser = serial.Serial(port, 9600, timeout=1)

ser.write(str.encode("T " + str(device) + "\\n"))
print(str(ser.readline()).split("'")[1][:-2])

while(True):
    if ser.readable():
        buffer += str(ser.readline()).split("'")[1][:-2]
        if buffer != "" and "OK\\r" in buffer: break

print("OK: " + buffer)