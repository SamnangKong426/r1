import serial
import re

class ComArduino:
    def __init__(self):
        self.arser = serial.Serial()
        self.arser.port = '/dev/ttyUSB0'
        self.arser.baudrate = 115200
        self.arser.timeout = 0.1
        self.arser.write_timeout = 0.1
        self.arser.setDTR(True)
        self.arser.open()
        self.arrx = bytes(0)

    def ar_read_from_port(self):
        while True:
            print("Reading from port")
            while self.arser.in_waiting > 0:
                global arrx
                arrx = self.arser.read(500)
                self.arser.flushInput()
                txt = str(arrx, 'utf-8')
                print(txt)
                
    def compare_strings(self, string1, string2):
        pattern = re.compile(string2)
        match = re.search(pattern, string1)
        if match:
            return True
        # else:
        #     print(f"'{string2}' not found in '{string1}'")

                
