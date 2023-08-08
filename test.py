import serial

ser = serial.Serial("/dev/cu.usbmodem21201", 9600, timeout=1)


try:
    while True:
        ser.write(str.encode("M\n"))

        if ser.readable():
            data = ser.readline()
            print(data)

except:
    ser.close()