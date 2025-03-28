import cv2
import os
import numpy as np

class TrafficSignDetector:
    def __init__(self, sign_type='stop'):
        """
        Args:
            sign_type: 标志类型 ('stop', 'left', 'right')
        """
        # 标志类型到模型文件的映射
        self.model_files = {
            'stop': 'stop.xml',
            'left': 'left.xml',
            'right': 'right.xml'
        }
        self.sign_type = sign_type
        
        # 加载对应的Haar级联分类器
        cascade_path = os.path.join(os.path.dirname(__file__), 
                                  f'../models/{self.model_files[sign_type]}')
        self.classifier = cv2.CascadeClassifier(cascade_path)
        if self.classifier.empty():
            raise ValueError(f"Error: Cascade classifier for {sign_type} failed to load")

    def detect(self, frame):
        """检测图像中的交通标志
        Args:
            frame: BGR格式的图像
        Returns:
            bool: 是否检测到标志
            list: 检测到的标志位置 [x, y, w, h]
        """
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 直方图均衡化以提高对比度
        gray = cv2.equalizeHist(gray)
        
        # 检测交通标志
        signs = self.classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # 如果检测到交通标志
        if len(signs) > 0:
            # 返回检测结果和第一个检测到的标志位置
            return True, signs[0].tolist()
        
        return False, []

    def draw_detection(self, frame, bbox):
        """在图像上绘制检测结果
        Args:
            frame: BGR格式的图像
            bbox: 边界框 [x, y, w, h]
        Returns:
            标注后的图像
        """
        if len(bbox) == 4:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f'{self.sign_type.title()} Sign', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        return frame