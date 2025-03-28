import cv2
import numpy as np
from perception.lane_detection import LaneDetector
from camera.camera_stream import CameraStream
from control.vehicle_control import VehicleController

import sys

class LaneKeepingProgram:
    def __init__(self):
        self.detector = LaneDetector()
        try:
            self.vehicle = VehicleController()
            self.vehicle.start_engine()
        except RuntimeError as e:
            print(f"Failed to initialize vehicle controller: {e}")
            raise
        self.default_speed = 20  # Speed in percentage (0-100)
        
    def process_frame(self, frame):
        try:
            steering_angle = self.detector.detect(frame)
            result = frame.copy()
            cv2.putText(result, f"Steering: {steering_angle:.1f}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            return steering_angle, result
        except Exception as e:
            print(f"Error processing frame: {e}")
            return 0, frame

    def run(self):
        camera = CameraStream()
        try:
            camera.start()
            self.vehicle.drive_forward(self.default_speed)
            
            while True:
                frame = camera.capture_frame()
                if frame is None:
                    print("Failed to read frame")
                    break
                    
                steering_angle, result = self.process_frame(frame)
                self.vehicle.adjust_steering(steering_angle)
                print(f"Steering angle: {steering_angle:.1f}")
                
                cv2.putText(result, f"Speed: {self.default_speed}%", 
                          (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("Program stopped by user")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.vehicle.stop()
            camera.stop()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    program = LaneKeepingProgram()
    program.run()
