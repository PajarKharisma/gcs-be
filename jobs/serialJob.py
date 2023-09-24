import threading
import serial
from config import context
from utils import formatter

class SerialThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.ser  = None

    def run(self):
        try:
            print("+++++++++ SETTING UP CONNECTION ++++++++")
            self.ser = serial.Serial(port=context.INPUT_VALUES['port'], baudrate=context.INPUT_VALUES['baudrate'], timeout=.1)
            while(context.INPUT_VALUES['app_connect']):
                rawData = serial.to_bytes(self.ser.readline()).decode('utf-8')
                rawData = rawData.strip()
                if not rawData.startswith("roll"):
                    continue
                data = formatter.formatData(rawData)
                if data is not None:
                    context.OUTPUT_VALUES = data
            print("******************* RELEASING CONNECTION *******************")
            self.ser.close()
            exit()
        except:
            print("Error")