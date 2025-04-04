import cv2
import numpy as np

class LaneDetector:
    def __init__(self):
        self.prev_steering = 0

    def detect(self, frame):
        height, width = frame.shape[:2]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)

        # 只取底部区域
        pct = 0.6
        roi = white_mask[int(height * pct):, :]
        edges = cv2.Canny(roi, 50, 150)

        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50,
                                minLineLength=60, maxLineGap=50)

        left_lines = []
        right_lines = []
        line_segments = []
        roi_offset = int(height * pct)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                x1, y1 = x1, y1 + roi_offset
                x2, y2 = x2, y2 + roi_offset
                line_segments.append((x1, y1, x2, y2))

                if x2 - x1 == 0:
                    continue  # 忽略垂直线

                slope = (y2 - y1) / (x2 - x1)
                if abs(slope) < 0.5:
                    continue  # 忽略平的线

                if slope < 0:
                    left_lines.append((x1, y1, x2, y2))
                else:
                    right_lines.append((x1, y1, x2, y2))

        left_avg = self._average_line(left_lines, height)
        right_avg = self._average_line(right_lines, height)

        # 可视化线段
        display_lines = []
        if left_avg:
            display_lines.append(left_avg)
        if right_avg:
            display_lines.append(right_avg)

        # 计算车道中心 → steering angle
        center_x = width // 2
        lane_center = center_x  # fallback: assume straight

        if left_avg and right_avg:
            lx1, ly1, lx2, ly2 = left_avg
            rx1, ry1, rx2, ry2 = right_avg
            lane_center = (lx2 + rx2) // 2
        elif left_avg:
            lx1, ly1, lx2, ly2 = left_avg
            lane_center = lx2 + 100
        elif right_avg:
            rx1, ry1, rx2, ry2 = right_avg
            lane_center = rx2 - 100

        deviation = lane_center - center_x
        steering = deviation / (width // 2) * 45  # 映射到 ±45°

        # 平滑处理
        steering = 0.8 * self.prev_steering + 0.2 * steering
        self.prev_steering = steering

        return steering, display_lines

    def _average_line(self, lines, height):
        if len(lines) == 0:
            return None

        x_coords = []
        y_coords = []
        for x1, y1, x2, y2 in lines:
            x_coords += [x1, x2]
            y_coords += [y1, y2]

        if len(x_coords) == 0 or len(y_coords) == 0:
            return None

        poly = np.polyfit(y_coords, x_coords, deg=1)
        y1 = height
        y2 = int(height * 0.6)
        x1 = int(np.polyval(poly, y1))
        x2 = int(np.polyval(poly, y2))
        return (x1, y1, x2, y2)
