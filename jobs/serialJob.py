import threading
from config import context
from dronekit import connect
import time
import logging
import math
import serial
import time

class SerialThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.vehicle = None
        self.stop_event = threading.Event()
        self.antena = None

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            logging.info(f"Connecting to vehicle on: {context.VALUES['port']}")
            logging.info(f"Baudrate: {context.VALUES['baudrate']}")
            while not self.stop_event.is_set():
                if context.VALUES['app_connect']:
                    if self.vehicle is None:
                        try:
                            logging.info("Attempting to connect to the vehicle...")
                            self.vehicle = connect(context.VALUES['port'], baud=context.VALUES['baudrate'], wait_ready=False)
                            logging.info('Attempting to connect to the antena...')
                            self.antena = serial.Serial(context.VALUES['antena_port'], context.VALUES['antena_baudrate'], timeout=1)
                        except PermissionError as e:
                            logging.error(f"Permission error connecting to {context.VALUES['port']}: {e}")
                            logging.error(f"Permission error connecting to {context.VALUES['antena_port']}: {e}")
                            self.stop()
                            return
                        except Exception as e:
                            logging.error(f"Error connecting to {context.VALUES['port']}: {e}")
                            logging.error(f"Error connecting to {context.VALUES['antena_port']}: {e}")
                            self.stop()
                            return

                    context.VALUES['pitch'] = self.vehicle.attitude.pitch
                    context.VALUES['roll'] = self.vehicle.attitude.roll
                    context.VALUES['yaw'] = self.vehicle.attitude.yaw
                    context.VALUES['alt'] = self.vehicle.location.global_relative_frame.alt
                    context.VALUES['lat'] = self.vehicle.location.global_relative_frame.lat
                    context.VALUES['long'] = self.vehicle.location.global_relative_frame.lon
                    context.VALUES['battery'] = 0 if self.vehicle.battery is None else self.vehicle.battery.level
                    context.VALUES['is_armable'] = self.vehicle.is_armable
                    context.VALUES['system_status'] = self.vehicle.system_status.state
                    context.VALUES['mode'] = self.vehicle.mode.name
                    context.VALUES['last_heartbeat'] = self.vehicle.last_heartbeat

                    azimuth = self.calculate_azimuth(context.VALUES['lat'], context.VALUES['long'], context.VALUES['antena_lat'], context.VALUES['antena_long'])
                    self.antena.write(str(azimuth).encode())
                else:
                    if self.vehicle is not None:
                        self.vehicle.close()
                        self.vehicle = None
                    if self.antena is not None:
                        self.antena.close()
                        self.antena = None
                time.sleep(0.5)

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received. Stopping thread.")
            if self.vehicle is not None:
                self.vehicle.close()
                self.vehicle = None
            self.stop()

        finally:
            if self.vehicle is not None:
                self.vehicle.close()
                self.vehicle = None
            logging.info("Thread stopped.")
    
    def calculate_azimuth(self, drone_lat, drone_lon, antenna_lat, antenna_lon):
        drone_lat = math.radians(drone_lat)
        drone_lon = math.radians(drone_lon)
        antenna_lat = math.radians(antenna_lat)
        antenna_lon = math.radians(antenna_lon)
        
        delta_lon = drone_lon - antenna_lon
        x = math.sin(delta_lon) * math.cos(drone_lat)
        y = math.cos(antenna_lat) * math.sin(drone_lat) - (math.sin(antenna_lat) * math.cos(drone_lat) * math.cos(delta_lon))
        
        azimuth = math.atan2(x, y)
        azimuth = math.degrees(azimuth)
        azimuth = (azimuth + 360) % 360  # Menjaga agar azimuth tetap dalam rentang 0-360 derajat
        
        return azimuth
