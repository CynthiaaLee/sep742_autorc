# -*- coding: utf-8 -*-
"""
@Author: Jieying Li
@Created Date: 2025-04-04 22:41:08
@Path: /main.py
"""


import logging
import os
import time
from datetime import datetime

import cv2

from control.vehicle_control import VehicleController
from logic.decision import DecisionMaker
from logic.perception_memory import PerceptionTracker
from perception.lane_detection import LaneDetector
from perception.traffic_light_detection import TrafficLightDetector
from perception.traffic_sign_detection import TrafficSignDetector
from utils.config import *


def save_frame(frame, directory="debug_frames"):
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    filename = f"{directory}/frame_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[INFO] Saved frame to {filename}")

class AutoDriver:
    def __init__(self, debug=False, video_path=None):
        self.debug = debug
        self.video_path = video_path
        self.use_video = video_path is not None
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('AutoDriver')

        self.frame_counter = 0
        self.detection_interval = 5  # Detect every N frames (originally 10, reduced for faster detection)
        self.last_stop_sign_result = (False, False, None)
        self.last_light_result = (None, None)

        try:
            self.camera = None
            self.video_cap = None
            self.vehicle = None
            self.lane_detector = LaneDetector()
            self.stop_sign_detector = TrafficSignDetector('stop')
            self.light_detector = TrafficLightDetector()
            self.decision_maker = DecisionMaker()
            self.stop_sign_tracker = PerceptionTracker()
            self.light_color_tracker = PerceptionTracker()

        except Exception as e:
            self.logger.error(f"Initialization error: {str(e)}")
            raise

    def __enter__(self):
        try:
            if self.use_video:
                self.video_cap = cv2.VideoCapture(self.video_path)
                if not self.video_cap.isOpened():
                    raise IOError(f"Cannot open video file: {self.video_path}")
                self.frame_source = self.video_cap
                self.fps = self.video_cap.get(cv2.CAP_PROP_FPS) or 30
                self.width = int(self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                self.height = int(self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            else:
                from camera.camera_stream import CameraStream
                self.camera_ctx = CameraStream()
                self.camera = self.camera_ctx.__enter__()
                self.frame_source = self.camera
                self.fps = 30  # Default camera frame rate
                self.width = self.camera.width
                self.height = self.camera.height

            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            os.makedirs("output", exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            filename = f"output/autodrive_result_{timestamp}.mp4"
            self.video_writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height))

            self.vehicle_ctx = VehicleController()
            self.vehicle = self.vehicle_ctx.__enter__()

            self.logger.info(f"VideoWriter initialized: {self.width}x{self.height} @ {self.fps}fps")

            return self

        except Exception as e:
            self.logger.error(f"Failed to initialize components: {str(e)}")
            self.__exit__(None, None, None)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.vehicle:
                self.vehicle_ctx.__exit__(exc_type, exc_val, exc_tb)
            if not self.use_video and self.camera:
                self.camera_ctx.__exit__(exc_type, exc_val, exc_tb)
            elif self.use_video and self.video_cap:
                self.video_cap.release()
            if self.video_writer:
                self.video_writer.release()
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
            raise

    def start(self):
        self.logger.info("Starting autonomous driving system")
        self.logger.info(f"debug mode: {self.debug}")
        try:
            while True:
                start_time = time.time()
                if self.use_video:
                    ret, frame = self.frame_source.read()
                    if not ret:
                        self.logger.info("End of video or frame error.")
                        break
                else:
                    frame = self.frame_source.capture_frame()
                    if frame is None:
                        self.logger.warning("Failed to capture frame")
                        continue

                self.frame_counter += 1

                if frame.shape[2] == 4:
                    self.logger.debug("Converting BGRA frame to BGR at input stage")
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                elif frame.shape[2] == 1:
                    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

                # Detect every detection_interval frames, skip others
                if self.frame_counter % self.detection_interval != 0:
                    # Still write the original frame (optional)
                    if self.video_writer:
                        self.video_writer.write(frame)
                    continue

                if self.use_video:
                    current_time_ms = self.frame_source.get(cv2.CAP_PROP_POS_MSEC)
                    minutes = int(current_time_ms // 60000)
                    seconds = int((current_time_ms % 60000) // 1000)
                    self.logger.info(f"[Video Time] {minutes:02d}:{seconds:02d}")

                t0 = time.time()
                steering_angle, lane_lines = self.lane_detector.detect(frame)
                t1 = time.time()
                is_stop_sign, is_stop_sign_close, stop_bbox = self.stop_sign_detector.detect(frame)
                t2 = time.time()
                light_color, light_box = self.light_detector.detect_by_sign_and_color(frame)
                t3 = time.time()

                # Update historical perception data
                self.stop_sign_tracker.update(is_stop_sign_close)
                self.light_color_tracker.update(light_color)

                # Determine stable states
                is_stop_sign_stable = self.stop_sign_tracker.recently_true(min_count=3)
                stable_light = self.light_color_tracker.most_common(min_count=2)

                if self.debug:
                    self.logger.info(
                        f"[Perception] Lane angle: {steering_angle:.2f}, "
                        f"is_stop_sign: {is_stop_sign}, is_stop_sign_stable: {is_stop_sign_stable}, "
                        f"stop_sign_close: {is_stop_sign_close}, stop_bbox: {stop_bbox}, "
                        f"light: {light_color}, stable light: {stable_light}, light_box: {light_box}"
                    )

                # Decision-making process
                decision = self.decision_maker.make_decision(
                    steering_angle, is_stop_sign_stable, stable_light
                )
                print(f"Decision: {decision}")
                t4 = time.time()
                self.logger.info(
                    f"[Profiling] Lane: {t1-t0:.3f}s, StopSign: {t2-t1:.3f}s, Light: {t3-t2:.3f}s, Other: {t4-t3:.3f}s"
                )
                # Execute control actions based on the decision
                if decision['action'] == 'stop':
                    self.vehicle.drive_neutral()
                    print("Stopping vehicle")
                else:
                    print("Driving vehicle")
                    print(f"Steering: {decision['steering']:.2f} → {decision['direction']} ({decision['strength']}%)")
                    # self.vehicle.drive_neutral()
                    self.vehicle.drive_forward()
                    self.vehicle.adjust_steering(decision['direction'], decision['strength'])

                # Visualization & output video frame
                if self.debug:
                    display_frame = frame.copy()
                    # Draw perception info
                    cv2.putText(display_frame, f"Steering: {steering_angle:.2f}", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    if is_stop_sign:
                        s_x, s_y, s_w, s_h = stop_bbox
                        cv2.rectangle(display_frame, (s_x, s_y), (s_x+s_w, s_y+s_h), (0, 100, 255), 2)
                    cv2.putText(display_frame, f"Stop Sign: {stop_bbox}, Close: {is_stop_sign_close}, Close&Stable: {is_stop_sign_stable}", (10, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    if light_box:
                        l_x, l_y, l_w, l_h = light_box
                        cv2.rectangle(display_frame, (l_x, l_y), (l_x+l_w, l_y+l_h), (255, 255, 0), 2)
                    cv2.putText(display_frame, f"Traffic Light: {light_color}, Stable Light: {stable_light}", (10, 140),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    cv2.putText(display_frame, f"Action: {decision['action']}", (10, 180),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.putText(display_frame, f"Direction: {decision['direction']}", (10, 220),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    cv2.putText(display_frame, f"Strength: {decision['strength']}%", (10, 260), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                    # ✅ Draw detected lane lines
                    for (x1, y1, x2, y2) in lane_lines:
                        cv2.line(display_frame, (x1, y1), (x2, y2), (0, 255, 255), 3)

                    # Write the video frame
                    if self.video_writer:
                        self.video_writer.write(display_frame)                    

                    # # Save key frames
                    # if is_stop_sign_stable or stable_light:
                    #     save_frame(display_frame)

                
                end_time = time.time()
                duration = end_time - start_time
                self.logger.info(f"[Timing] Decision cycle time: {duration:.3f}s")

        except KeyboardInterrupt:
            self.logger.info("Manual stop triggered")
        except Exception as e:
            self.logger.error(f"Runtime error: {str(e)}")
        finally:
            self.logger.info("Shutting down system...")
            try:
                self.vehicle.stop()
                self.vehicle.steering_center()
            except Exception as e:
                self.logger.warning(f"Error during vehicle shutdown: {e}")

            try:
                if self.video_writer:
                    self.video_writer.release()
                    self.logger.info("VideoWriter released successfully.")
            except Exception as e:
                self.logger.error(f"Error releasing VideoWriter: {e}")

            if self.debug:
                cv2.destroyAllWindows()

            self.logger.info("System shutdown complete.")

def run(debug=False, video_path=None):
    with AutoDriver(debug=debug, video_path=video_path) as driver:
        driver.start()

if __name__ == '__main__':
    try:
        video_path = None  # ← Use camera
        # video_path = "models/test_video.mp4"  # ← Or replace with your video path
        run(debug=True, video_path=video_path)
    except Exception as e:
        logging.error(f"System error: {str(e)}")
