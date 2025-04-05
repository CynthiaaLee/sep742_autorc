import glob
import os
import unittest

import cv2
import numpy as np

from perception.traffic_light_detection import TrafficLightDetector


class TestTrafficLightDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = TrafficLightDetector()
        
        # Set the directory for test images
        cls.test_dir = os.path.join(os.path.dirname(__file__), '../models/lights')
        cls.output_dir = os.path.join(os.path.dirname(__file__), '../output/lights')
        os.makedirs(cls.output_dir, exist_ok=True)
        
        # Retrieve all test images
        cls.test_images = glob.glob(os.path.join(cls.test_dir, '*.jpg')) + \
                         glob.glob(os.path.join(cls.test_dir, '*.png'))
        
        if not cls.test_images:
            raise FileNotFoundError(f"No test images found in {cls.test_dir}")
        print(f"\nFound {len(cls.test_images)} test images")

    def test_real_images(self):
        """Test detection on real traffic light images"""
        for image_path in self.test_images:
            with self.subTest(image=image_path):
                print(f"\nTesting image: {os.path.basename(image_path)}")
                
                # Read the image
                image = cv2.imread(image_path)
                self.assertIsNotNone(image, f"Failed to load image: {image_path}")
                
                # Detect traffic lights
                color, bbox = self.detector.detect_by_sign_and_color(image)
                print(f"Detected color: {color}")
                print(f"Bounding box: {bbox}")
                
                # Save the result image
                if color and bbox:
                    result = self.detector.draw_detection(image.copy(), color, bbox)
                    output_path = os.path.join(
                        self.output_dir,
                        f"result_{os.path.basename(image_path)}"
                    )
                    cv2.imwrite(output_path, result)
                    print(f"Result saved to: {output_path}")
                
                # Verify detection results
                self.assertIsNotNone(color, f"No traffic light detected in {image_path}")

if __name__ == '__main__':
    unittest.main()
