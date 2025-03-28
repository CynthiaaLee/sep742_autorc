import unittest
import cv2
import os
import numpy as np
from perception.lane_detection import LaneDetector

class TestLaneDetector(unittest.TestCase):
    def setUp(self):
        # 初始化 LaneDetector 实例
        self.detector = LaneDetector()
        # 测试图片目录路径
        self.test_image_dir = os.path.join(
            os.path.dirname(__file__), '../models/lane'
        )
        # 确保测试目录存在
        if not os.path.exists(self.test_image_dir):
            raise FileNotFoundError(f"Test directory not found at {self.test_image_dir}")

    def get_image_files(self):
        """获取目录下所有图片文件"""
        image_extensions = ['.jpg', '.jpeg', '.png']
        image_files = []
        for file in os.listdir(self.test_image_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(self.test_image_dir, file))
        return image_files

    def test_lane_detection(self):
        image_files = self.get_image_files()
        self.assertTrue(len(image_files) > 0, "No image files found in test directory")

        for image_path in image_files:
            with self.subTest(image_path=image_path):
                # 加载测试图片
                test_image = cv2.imread(image_path)
                if test_image is None:
                    self.fail(f"Failed to load test image from {image_path}")
                
                # 调用 detect 方法
                steering_angle = self.detector.detect(test_image)
                
                # 打印检测结果
                print(f"Image: {os.path.basename(image_path)}, Detected steering angle:", steering_angle)
                
                # 检查返回的转向角是否在合理范围内（例如 -45 到 45 度）
                self.assertTrue(-45 <= steering_angle <= 45, 
                              f"Steering angle {steering_angle} is out of range!")

if __name__ == '__main__':
    unittest.main()