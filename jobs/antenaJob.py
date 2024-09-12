import threading
from config import context
import time
import logging
import math
import serial
import time

class AntenaThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stop_event = threading.Event()
        self.antena = None
        self.previous_direction = 0

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            logging.info(f"Connecting to Antena on: {context.VALUES['antena_port']}")
            logging.info(f"Baudrate: {context.VALUES['antena_baudrate']}")
            while not self.stop_event.is_set():
                if context.VALUES['app_connect']:
                    if self.antena is None:
                        try:
                            logging.info('Attempting to connect to the antena...')
                            self.antena = serial.Serial(context.VALUES['antena_port'], context.VALUES['antena_baudrate'], timeout=1)
                        except PermissionError as e:
                            logging.error(f"Permission error connecting to {context.VALUES['antena_port']}: {e}")
                            self.stop()
                            return
                        except Exception as e:
                            logging.error(f"Error connecting to {context.VALUES['antena_port']}: {e}")
                            self.stop()
                            return
                    bearing = self.calculate_bearing(context.VALUES['antena_lat'], context.VALUES['antena_long'], context.VALUES['lat'], context.VALUES['long'])
                    logging.info(f"Antena bearing is: {bearing}")
                    direction = self.closest_cardinal_direction(bearing)
                    logging.info(f"Antena direction is: {direction}")
                    if (self.previous_direction != direction):
                        movement = direction - self.previous_direction
                        self.antena.write(str(movement).encode())
                        self.previous_direction = direction
                else:
                    if self.antena is not None:
                        self.antena.close()
                        self.antena = None
                time.sleep(2)

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received. Stopping antena thread.")
            if self.antena is not None:
                self.antena.close()
                self.antena = None
            self.stop()

        finally:
            if self.antena is not None:
                self.antena.close()
                self.antena = None
            logging.info("Thread stopped.")
    
    def degrees_to_radians(self, degrees):
        return degrees * math.pi / 180

    def calculate_bearing(self, lat1, lon1, lat2, lon2):
        lat1 = self.degrees_to_radians(lat1)
        lon1 = self.degrees_to_radians(lat1)
        lat2 = self.degrees_to_radians(lat2)
        lon2 = self.degrees_to_radians(lon2)
        d_lon = lon2 - lon1
        x = math.sin(d_lon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(d_lon))
        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        
        return compass_bearing
    
    def closest_cardinal_direction(self, bearing):
        cardinals = [0, 90, 180, 270]
        closest = min(cardinals, key=lambda x: abs(bearing - x))
        return closest

