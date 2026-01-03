import serial
import time
data = serial.Serial(
                    'COM3',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                    )

def Send(a):
  data.write(str.encode(a))
  print('sent............')

def Read():
    print("reading")
    while True:
        Data = data.readline()
        Data = Data.decode('utf-8', 'ignore').strip()  # remove \r, \n, and spaces
        # print("Raw data is ---- {}  ---".format(Data))
        Data = Data.split(',')
        print(Data)
        if len(Data) == 4:
            break
    return Data

# da=Read()

# print(da)
