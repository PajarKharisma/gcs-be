import threading
from config import context
from dronekit import connect, VehicleMode
import time
import os

class SerialThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.vehicle = None
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set() 

    def run(self):
        try:
            print("Connecting to vehicle on: %s" % context.VALUES['port'])
            print("Baudrate: %s" % context.VALUES['baudrate'])
            while not self.stop_event.is_set():
                if context.VALUES['app_connect']:
                    if self.vehicle is None:
                        self.vehicle = connect(context.VALUES['port'], baud=context.VALUES['baudrate'], wait_ready=False)
                    context.VALUES['pitch'] = self.vehicle.attitude.pitch
                    context.VALUES['roll'] = self.vehicle.attitude.roll
                    context.VALUES['yaw'] = self.vehicle.attitude.yaw
                    context.VALUES['alt'] = self.vehicle.location.global_relative_frame.alt
                    context.VALUES['lat'] = self.vehicle.location.global_relative_frame.lat
                    context.VALUES['long'] = self.vehicle.location.global_relative_frame.lon
                    context.VALUES['battery'] = self.vehicle.battery.voltage
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
            # Disconnect from the vehicle
            if self.vehicle is not None:
                self.vehicle.close()
                self.vehicle = None
            self.stop()

        finally:
            # Ensure the vehicle is disconnected when stopping
            if self.vehicle is not None:
                self.vehicle.close()
