import cv2
import numpy as np
import logging
from camera.camera_stream import CameraStream
from control.vehicle_control import VehicleController
from perception.lane_detection import LaneDetector
from perception.traffic_sign_detection import TrafficSignDetector
from perception.traffic_light_detection import TrafficLightDetector
from logic.decision import DecisionMaker
from utils.config import *
import time

class AutoDriver:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('AutoDriver')
        
        try:
            self.camera = CameraStream(resolution=CAMERA_RESOLUTION, framerate=FRAME_RATE)
            self.vehicle = VehicleController()
            self.lane_detector = LaneDetector()
            self.sign_detector = TrafficSignDetector()
            self.light_detector = TrafficLightDetector()
            self.decision_maker = DecisionMaker()
        except Exception as e:
            self.logger.error(f"Initialization error: {str(e)}")
            raise
            
    def start(self):
        self.logger.info("Starting autonomous driving system")
        self.vehicle.start_engine()
        
        with self.camera as cam:
            try:
                while True:
                    ret, frame = cam.read()
                    if not ret:
                        self.logger.warning("Failed to capture frame")
                        continue
                        
                    # Perception
                    steering_angle = self.lane_detector.detect(frame)
                    sign = self.sign_detector.detect(frame)
                    light = self.light_detector.detect(frame)
                    # Decision making
                    decision = self.decision_maker.make_decision(
                        steering_angle, sign, light
                    )
                    
                    # Control execution
                    if decision['action'] == 'stop':
                        self.vehicle.stop()
                    else: # TODO: slow down when turning
                        self.vehicle.drive_forward()
                        self.vehicle.adjust_steering(decision['steering'])
                        
                    time.sleep(0.05)  # Control loop rate limiting
                    
            except KeyboardInterrupt:
                self.logger.info("Manual stop triggered")
            except Exception as e:
                self.logger.error(f"Runtime error: {str(e)}")
            finally:
                self.vehicle.stop()
                self.logger.info("System shutdown complete")

if __name__ == '__main__':
    try:
        driver = AutoDriver()
        driver.start()
    except Exception as e:
        logging.error(f"System error: {str(e)}")
