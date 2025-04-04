import cv2
import numpy as np
# from ultralytics import YOLO
from PIL import Image
from perception.traffic_sign_detection import TrafficSignDetector


class TrafficLightDetector:
    def __init__(self, model_path='models/best_traffic_nano_yolo.pt'):
        # 加载 YOLO 模型
        # self.model = YOLO(model_path)
        self.sign_detector = TrafficSignDetector(sign_type='light')  # 加载light的haar分类器
        
        # 保留原有的 HSV 颜色范围作为备用
        self.red_range = [([0, 100, 100], [10, 255, 255]), 
                         ([160, 100, 100], [180, 255, 255])]
        self.yellow_range = ([20, 100, 100], [30, 255, 255])
        self.green_range = ([40, 100, 100], [80, 255, 255])



    def detect_by_sign_and_color(self, image):
        """
        使用Haar cascade检测疑似交通灯，再分析该区域的颜色判断灯色
        返回: (color, bbox)
        """
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
                if area > max_area and area > 50:  # 阈值可调
                    max_area = area
                    detected_color = color
        
        if detected_color:
            return detected_color, bbox
        else:
            return None, None

    # def detect(self, image):
    #     """
    #     使用 YOLO 模型检测交通信号灯
    #     返回: (color, bbox), color为'red', 'yellow', 'green'或None
    #     """
    #     # 运行 YOLO 检测
    #     # image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    #     results = self.model.predict(source=image, conf=0.25)
        
    #     if not results or len(results) == 0:
    #         return self._detect_by_color(image)  # 使用颜色检测作为备用
            
    #     # 获取最高置信度的检测结果
    #     result = results[0]
    #     if len(result.boxes) == 0:
    #         return None, None
            
    #     # 获取边界框和类别
    #     box = result.boxes[0]
    #     cls_id = int(box.cls[0])
    #     conf = float(box.conf[0])
        
    #     # 映射类别ID到颜色
    #     color_map = {0: 'red', 1: 'yellow', 2: 'green'}
    #     color = color_map.get(cls_id)
        
    #     # 转换边界框格式
    #     x1, y1, x2, y2 = map(int, box.xyxy[0])
    #     bbox = (x1, y1, x2-x1, y2-y1)
        
    #     return color, bbox

    # def _detect_by_color(self, image):
    #     """原有的基于颜色的检测方法作为备用"""
    #     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
    #     # 检测各种颜色
    #     red_mask = self._detect_color(hsv, self.red_range)
    #     yellow_mask = self._detect_color(hsv, [self.yellow_range])
    #     green_mask = self._detect_color(hsv, [self.green_range])

    #     # 确定最强的信号
    #     masks = {"red": red_mask, "yellow": yellow_mask, "green": green_mask}
    #     detected_color = None
    #     max_area = 0
    #     bbox = None

    #     for color, mask in masks.items():
    #         contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, 
    #                                      cv2.CHAIN_APPROX_SIMPLE)
    #         for cnt in contours:
    #             area = cv2.contourArea(cnt)
    #             if area > max_area and area > 100:  # 最小面积阈值
    #                 max_area = area
    #                 detected_color = color
    #                 bbox = cv2.boundingRect(cnt)

    #     return detected_color, bbox

    def _detect_color(self, hsv, ranges):
        """检测特定颜色范围"""
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in ranges:
            if isinstance(lower, (list, tuple)):
                color_mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                mask = cv2.bitwise_or(mask, color_mask)
        return mask

    def draw_detection(self, image, color, bbox):
        """在图像上绘制检测结果"""
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
        """处理单张图片并显示/保存结果"""
        # 读取图片
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        else:
            image = image_path
            
        # 检测交通灯
        color, bbox = self.detect(image)
        
        if color and bbox:
            # 绘制结果
            result = self.draw_detection(image.copy(), color, bbox)
            
            # 转换为PIL图像以显示
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(result_rgb)
            
            # 保存结果
            if save_path:
                im.save(save_path)
            
            # 显示结果
            im.show()
            
            return color, bbox
        return None, None
