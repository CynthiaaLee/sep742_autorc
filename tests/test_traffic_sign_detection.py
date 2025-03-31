import unittest
import cv2
import os
import glob
from perception.traffic_sign_detection import TrafficSignDetector

class TestTrafficSignDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 从环境变量获取 sign_type 参数，默认为 'right'
        cls.sign_type = os.getenv('SIGN_TYPE', 'right')
        print(f"\nInitializing tests for {cls.sign_type} sign detection")
        
        cls.detector = TrafficSignDetector(sign_type=cls.sign_type)
        
        # 查找所有匹配的测试图片
        search_pattern = os.path.join(
            os.path.dirname(__file__), 
            f'../models/{cls.sign_type}/*.png'
        )
        print(f"Looking for test images in: {search_pattern}")
        
        cls.test_images = glob.glob(search_pattern)
        print(f"Found {len(cls.test_images)} test images")
        for img in cls.test_images:
            print(f"  - {os.path.basename(img)}")
            
        if not cls.test_images:
            raise FileNotFoundError(f"No test images found for {cls.sign_type}")


    def test_sign_detection(self):
        for test_image_path in self.test_images:
            with self.subTest(image=test_image_path):                
                # 加载测试图片
                test_image = cv2.imread(test_image_path)
                if test_image is None:
                    self.fail(f"Failed to load test image from {test_image_path}")
                
                # Validate image dimensions
                h, w = test_image.shape[:2]
                if h <= 0 or w <= 0:
                    self.fail(f"Invalid image dimensions: {w}x{h}")
                
                # 检测标志
                detected, bbox = self.detector.detect(test_image)
                base_name = os.path.basename(test_image_path)

                # 如果检测到，绘制结果并保存
                if detected:
                    result_image = self.detector.draw_detection(test_image.copy(), bbox)
                    result_path = os.path.join(
                        os.path.dirname(__file__), 
                        f'../output/{self.sign_type}_{base_name}'
                    )
                    os.makedirs(os.path.dirname(result_path), exist_ok=True)
                    cv2.imwrite(result_path, result_image)
                print(f"Test image: {base_name}")
                print("Detection result:", detected)
                print("Bounding box:", bbox)

                self.assertTrue(detected, 
                    f"{self.sign_type} sign was not detected in {base_name}")

    def test_video_sign_detection(self):
        video_path = os.path.join(os.path.dirname(__file__), '../models/test_video.mp4')
        output_path = os.path.join(os.path.dirname(__file__), f'../output/{self.sign_type}_result_video.mp4')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self.fail(f"Failed to open video file: {video_path}")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detected, bbox = self.detector.detect(frame)
            if detected:
                frame = self.detector.draw_detection(frame, bbox)

                x, y, w, h = bbox
                label = f"{self.sign_type.title()} Sign (w={w}, h={h})"
                cv2.putText(frame, label, (x, y + h + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)

            out.write(frame)
            frame_idx += 1
            if frame_idx % 30 == 0:
                print(f"Processed {frame_idx} frames")

        cap.release()
        out.release()
        print(f"Video processed and saved to {output_path}")


if __name__ == '__main__':
    unittest.main()
