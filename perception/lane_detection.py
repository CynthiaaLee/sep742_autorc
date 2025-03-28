import cv2
import numpy as np

class LaneDetector:
    def __init__(self):
        self.prev_steering = 0
        
    def detect(self, frame):
        # 转换到HSV色彩空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)
        
        # 车道线掩码（假设为白色或黄色）
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # 图像预处理
        roi = white_mask[white_mask.shape[0]//2:, :]
        edges = cv2.Canny(roi, 50, 150)
        
        # 霍夫变换检测直线
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50,
                               minLineLength=100, maxLineGap=50)
        
        if lines is not None:
            # 计算平均转向角
            angles = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2-y1, x2-x1) * 180 / np.pi
                if abs(angle) < 45:  # 过滤垂直线
                    angles.append(angle)
            
            if angles:
                steering = np.mean(angles)
                # 平滑处理
                steering = 0.8 * self.prev_steering + 0.2 * steering
                self.prev_steering = steering
                return steering
                
        return self.prev_steering
