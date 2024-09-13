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
                        except PermissionError as e:
                            logging.error(f"Permission error connecting to {context.VALUES['port']}: {e}")
                            self.stop()
                            return
                        except Exception as e:
                            logging.error(f"Error connecting to {context.VALUES['port']}: {e}")
                            self.stop()
                            return

                    context.VALUES['pitch'] = self.vehicle.attitude.pitch
                    context.VALUES['roll'] = self.vehicle.attitude.roll
                    context.VALUES['yaw'] = self.vehicle.attitude.yaw
                    context.VALUES['alt'] = self.vehicle.location.global_relative_frame.alt
                    context.VALUES['lat'] = self.vehicle.location.global_relative_frame.lat
                    context.VALUES['long'] = self.vehicle.location.global_relative_frame.lon
                    context.VALUES['battery'] = 0 if self.vehicle.battery is None else self.vehicle.battery.voltage
                    context.VALUES['is_armable'] = self.vehicle.is_armable
                    context.VALUES['system_status'] = self.vehicle.system_status.state
                    context.VALUES['mode'] = self.vehicle.mode.name
                    context.VALUES['last_heartbeat'] = self.vehicle.last_heartbeat
                else:
                    if self.vehicle is not None:
                        self.vehicle.close()
                        self.vehicle = None
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
