import unittest
import cv2
import os
import glob
import numpy as np
from perception.traffic_light_detection import TrafficLightDetector

class TestTrafficLightDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = TrafficLightDetector()
        
        # 设置测试图片目录
        cls.test_dir = os.path.join(os.path.dirname(__file__), '../models/lights')
        cls.output_dir = os.path.join(os.path.dirname(__file__), '../output/lights')
        os.makedirs(cls.output_dir, exist_ok=True)
        
        # 获取所有测试图片
        cls.test_images = glob.glob(os.path.join(cls.test_dir, '*.jpg')) + \
                         glob.glob(os.path.join(cls.test_dir, '*.png'))
        
        if not cls.test_images:
            raise FileNotFoundError(f"No test images found in {cls.test_dir}")
        print(f"\nFound {len(cls.test_images)} test images")

    def test_real_images(self):
        """测试实际交通信号灯图片"""
        for image_path in self.test_images:
            with self.subTest(image=image_path):
                print(f"\nTesting image: {os.path.basename(image_path)}")
                
                # 读取图片
                image = cv2.imread(image_path)
                self.assertIsNotNone(image, f"Failed to load image: {image_path}")
                
                # 检测交通信号灯
                color, bbox = self.detector.detect(image)
                print(f"Detected color: {color}")
                print(f"Bounding box: {bbox}")
                
                # 保存结果图片
                if color and bbox:
                    result = self.detector.draw_detection(image.copy(), color, bbox)
                    output_path = os.path.join(
                        self.output_dir,
                        f"result_{os.path.basename(image_path)}"
                    )
                    cv2.imwrite(output_path, result)
                    print(f"Result saved to: {output_path}")
                
                # 验证检测结果
                self.assertIsNotNone(color, f"No traffic light detected in {image_path}")

    def test_color_detection(self):
        """测试基础颜色检测"""
        # 创建测试图像
        test_colors = {
            'red': (0, 0, 255),
            'yellow': (0, 255, 255),
            'green': (0, 255, 0)
        }

        for expected_color, bgr in test_colors.items():
            # 创建单色测试图像
            test_image = np.zeros((100, 100, 3), dtype=np.uint8)
            cv2.circle(test_image, (50, 50), 20, bgr, -1)

            # 检测
            detected_color, bbox = self.detector.detect(test_image)
            
            # 验证结果
            self.assertEqual(detected_color, expected_color,
                           f"Failed to detect {expected_color} light")
            self.assertIsNotNone(bbox,
                               f"Failed to get bbox for {expected_color} light")

if __name__ == '__main__':
    unittest.main()
