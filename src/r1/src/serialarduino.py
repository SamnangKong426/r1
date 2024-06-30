import serial
import re

class SerialArduino:
    def __init__(self):
        self.arser = serial.Serial()
        self.arser.port = '/dev/ttyUSB0'
        self.arser.baudrate = 115200
        self.arser.timeout = 0.02
        self.arser.write_timeout = 0.1
        self.arser.setDTR(True)
        self.arser.open()
        self.arrx = bytes(0)
        self.msg = ''

    def ar_read_from_port(self):
        while True:
            while self.arser.in_waiting > 0:

                self.arrx = self.arser.read(500)
                self.arser.flushInput()
                txt = str(self.arrx, 'utf-8')
                self.msg = txt
                # print(txt)

                # try:
                # {"ch":[1500,1500,1500,1500,1000,1000,1000,1000,1500,1500,1500,1500,874,874,874,874]}                #               joystick = 1500
                #               button = 1000
                #               switch = 1500
                #     data = json.loads(txt)
                #     print(data)
                # except:
                #     print("Error loading JSON")

    @staticmethod
    def compare_strings(string1, string2):
        pattern = re.compile(string2)
        match = re.search(pattern, string1)
        if match:
            return True
        # else:
        #     print(f"'{string2}' not found in '{string1}'")