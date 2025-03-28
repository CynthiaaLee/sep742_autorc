import unittest
import cv2
import os
import sys
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

if __name__ == '__main__':
    unittest.main()
