import logging
from camera.camera_stream import CameraStream
from control.vehicle_control import VehicleController
from perception.lane_detection import LaneDetector
from perception.traffic_sign_detection import TrafficSignDetector
from perception.traffic_light_detection import TrafficLightDetector
from logic.decision import DecisionMaker
from utils.config import *
import time
from datetime import datetime
import os
import cv2

def save_frame(frame, directory="debug_frames"):
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    filename = f"{directory}/frame_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[INFO] Saved frame to {filename}")

class AutoDriver:
    def __init__(self, debug=False):
        self.debug = debug
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('AutoDriver')
        
        try:
            self.camera = None
            self.vehicle = None
            self.lane_detector = LaneDetector()
            self.sign_detector = TrafficSignDetector()
            self.light_detector = TrafficLightDetector()
            self.decision_maker = DecisionMaker()
        except Exception as e:
            self.logger.error(f"Initialization error: {str(e)}")
            raise

    def __enter__(self):
        try:
            self.camera_ctx = CameraStream()
            self.vehicle_ctx = VehicleController()
            self.vehicle = self.vehicle_ctx.__enter__()
            self.camera = self.camera_ctx.__enter__()
            return self
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {str(e)}")
            self.__exit__(None, None, None)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.vehicle:
                self.vehicle_ctx.__exit__(exc_type, exc_val, exc_tb)
            if self.camera:
                self.camera_ctx.__exit__(exc_type, exc_val, exc_tb)
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
            raise

    def start(self):
        self.logger.info("Starting autonomous driving system")
        self.logger.info(f"debug mode: {self.debug}")
        try:
            while True:
                frame = self.camera.capture_frame()
                if frame is None:
                    self.logger.warning("Failed to capture frame")
                    continue

                # Perception
                steering_angle = self.lane_detector.detect(frame)
                sign = self.sign_detector.detect(frame)
                light = self.light_detector.detect(frame)

                if self.debug:
                    self.logger.info(f"[Perception] Lane angle: {steering_angle}, Sign: {sign}, Light: {light}")

                # Decision making
                decision = self.decision_maker.make_decision(
                    steering_angle, sign, light
                )
                print(f"Decision: {decision}")

                # Control execution
                if decision['action'] == 'stop':
                    self.vehicle.stop()
                else: # TODO: slow down when turning
                    self.vehicle.drive_forward()
                    self.vehicle.adjust_steering(decision['steering'])
                    

                if self.debug:
                    save_frame(frame)
                    # import cv2
                    # display_frame = frame.copy()
                    # cv2.putText(display_frame, f"Steering: {decision['steering']}", (10, 30),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    # cv2.putText(display_frame, f"Action: {decision['action']}", (10, 60),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    # cv2.imshow("AutoDriver Debug View", display_frame)
                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                    #     self.logger.info("Debug mode quit requested (press 'q')")
                    #     break

                time.sleep(1)  # Control loop rate limiting
                
        except KeyboardInterrupt:
            self.logger.info("Manual stop triggered")
        except Exception as e:
            self.logger.error(f"Runtime error: {str(e)}")
        finally:
            self.vehicle.stop()
            if self.debug:
                import cv2
                cv2.destroyAllWindows()
            self.logger.info("System shutdown complete")

def run(debug=False):
    with AutoDriver(debug=debug) as driver:
        driver.start()

if __name__ == '__main__':
    try:
        run(debug=True)
    except Exception as e:
        logging.error(f"System error: {str(e)}")
