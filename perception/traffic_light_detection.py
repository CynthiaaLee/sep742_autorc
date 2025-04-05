import cv2
import numpy as np
from PIL import Image

from perception.traffic_sign_detection import TrafficSignDetector


class TrafficLightDetector:
    def __init__(self):
        self.sign_detector = TrafficSignDetector(sign_type='light')
        self.red_range = [([0, 100, 100], [10, 255, 255]), 
                         ([160, 100, 100], [180, 255, 255])]
        self.yellow_range = ([20, 100, 100], [30, 255, 255])
        self.green_range = ([40, 100, 100], [80, 255, 255])



    def detect_by_sign_and_color(self, image):
        """
        Using Haar cascade to detect suspected traffic lights, then analyze the color of that area
        to determine the light color.
        Returns: (color, bbox)"""
        found, _, bbox = self.sign_detector.detect(image)
        if not found or not bbox:
            return None, None
        
        x, y, w, h = bbox
        roi = image[y:y+h, x:x+w]
        
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        red_mask = self._detect_color(hsv_roi, self.red_range)
        yellow_mask = self._detect_color(hsv_roi, [self.yellow_range])
        green_mask = self._detect_color(hsv_roi, [self.green_range])
        
        masks = {"red": red_mask, "yellow": yellow_mask, "green": green_mask}
        max_area = 0
        detected_color = None
        
        for color, mask in masks.items():
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area and area > 50:
                    max_area = area
                    detected_color = color
        
        if detected_color:
            return detected_color, bbox
        else:
            return None, None

    def _detect_color(self, hsv, ranges):
        """Detect specific color ranges"""
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in ranges:
            if isinstance(lower, (list, tuple)):
                color_mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                mask = cv2.bitwise_or(mask, color_mask)
        return mask

    def draw_detection(self, image, color, bbox):
        """Draw the detection result on the image"""
        if bbox is None:
            return image

        x, y, w, h = bbox
        color_map = {
            "red": (0, 0, 255),
            "yellow": (0, 255, 255),
            "green": (0, 255, 0)
        }
        
        draw_color = color_map.get(color, (255, 255, 255))
        cv2.rectangle(image, (x, y), (x + w, y + h), draw_color, 2)
        cv2.putText(image, color, (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, draw_color, 2)
        
        return image

    def process_image(self, image_path, save_path=None):
        """Process a single image and display/save the result"""
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            image = image_path
            
        color, bbox = self.detect(image)
        if color and bbox:
            result = self.draw_detection(image.copy(), color, bbox)
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(result_rgb)

            if save_path:
                im.save(save_path)
            
            im.show()
            
            return color, bbox
        return None, None
