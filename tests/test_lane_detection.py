import unittest
import cv2
import os
import numpy as np
from perception.lane_detection import LaneDetector

class TestLaneDetector(unittest.TestCase):
    def setUp(self):
        self.detector = LaneDetector()
        self.test_image_dir = os.path.join(
            os.path.dirname(__file__), '../models/lane'
        )
        if not os.path.exists(self.test_image_dir):
            raise FileNotFoundError(f"Test directory not found at {self.test_image_dir}")

        self.output_dir = os.path.join(os.path.dirname(__file__), '../output/lane_detection')
        os.makedirs(self.output_dir, exist_ok=True)

    def get_image_files(self):
        image_extensions = ['.jpg', '.jpeg', '.png']
        return [
            os.path.join(self.test_image_dir, f)
            for f in os.listdir(self.test_image_dir)
            if any(f.lower().endswith(ext) for ext in image_extensions)
        ]

    def test_lane_detection(self):
        image_files = self.get_image_files()
        self.assertTrue(len(image_files) > 0, "No image files found in test directory")

        for image_path in image_files:
            with self.subTest(image_path=image_path):
                test_image = cv2.imread(image_path)
                if test_image is None:
                    self.fail(f"Failed to load test image from {image_path}")
                
                # 获取角度 + 车道线坐标
                steering_angle, lines = self.detector.detect(test_image)

                print(f"Image: {os.path.basename(image_path)}, Detected steering angle: {steering_angle:.2f}")
                self.assertTrue(-45 <= steering_angle <= 45,
                                f"Steering angle {steering_angle} is out of range!")

                # 可视化
                vis_image = test_image.copy()
                cv2.putText(vis_image, f"Steering: {steering_angle:.2f}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

                for (x1, y1, x2, y2) in lines:
                    cv2.line(vis_image, (x1, y1), (x2, y2), (0, 255, 255), 2)

                output_path = os.path.join(self.output_dir, os.path.basename(image_path))
                cv2.imwrite(output_path, vis_image)

    def test_lane_detection_on_video(self):
        video_path = os.path.join(os.path.dirname(__file__), "../models/test_video.mp4")
        output_path = os.path.join(os.path.dirname(__file__), "../output/lane_detection_result.mp4")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self.fail(f"Cannot open video file: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_idx = 0
        detection_interval = int(fps // 4)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 每隔一定帧检测
            if frame_idx % detection_interval == 0:
                steering_angle, lines = self.detector.detect(frame)
                vis_frame = frame.copy()

                # Draw steering
                cv2.putText(vis_frame, f"Steering: {steering_angle:.2f}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

                # Draw lanes
                for (x1, y1, x2, y2) in lines:
                    cv2.line(vis_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            else:
                vis_frame = frame

            out.write(vis_frame)
            frame_idx += 1

        cap.release()
        out.release()
        print(f"[✅] Detection video saved to: {output_path}")

if __name__ == '__main__':
    unittest.main()
