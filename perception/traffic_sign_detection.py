# -*- coding: utf-8 -*-
"""
@Author: Jieying Li
@Created Date: 2025-04-04 22:41:08
@Path: /perception/traffic_sign_detection.py
"""


import os

import cv2

from utils.config import MIN_STOP_SIGN_WIDTH


class TrafficSignDetector:
    def __init__(self, sign_type='stop'):
        """
        Args:
            sign_type: Type of sign ('stop', 'left', 'right')
        """
        # Mapping of sign types to model files
        self.model_files = {
            'stop': 'stop.xml',
            'left': 'left.xml',
            'right': 'right.xml',
            'light': 'light.xml',
        }
        self.sign_type = sign_type
        
        # Load the corresponding Haar cascade classifier
        cascade_path = os.path.join(os.path.dirname(__file__), 
                                  f'../models/{self.model_files[sign_type]}')
        self.classifier = cv2.CascadeClassifier(cascade_path)
        if self.classifier.empty():
            raise ValueError(f"Error: Cascade classifier for {sign_type} failed to load")

    def detect(self, frame):
        """Detect traffic signs in the image
        Args:
            frame: Image in BGR format
        Returns:
            bool: Whether a sign is detected
            list: Detected sign position [x, y, w, h]
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Histogram equalization to improve contrast
        gray = cv2.equalizeHist(gray)
        
        # Detect traffic signs
        signs = self.classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        is_sign = False
        is_close = False

        # If traffic signs are detected
        if len(signs) > 0:
            is_sign = True
            _, _, w, _ = signs[0].tolist()
            if w >= MIN_STOP_SIGN_WIDTH:  # Assume width greater than 60 pixels is close
                is_close = True
            # Return detection result and the first detected sign position
            return is_sign, is_close, signs[0].tolist()
        
        return is_sign, is_close, []

    def draw_detection(self, frame, bbox):
        """Draw detection results on the image
        Args:
            frame: Image in BGR format
            bbox: Bounding box [x, y, w, h]
        Returns:
            Annotated image
        """
        if len(bbox) == 4:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'{self.sign_type.title()} Sign', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        return frame