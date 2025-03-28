# Configuration parameters for autonomous RC car

# Camera Settings
CAMERA_RESOLUTION = (640, 480)
FRAME_RATE = 30
CAMERA_FLIP = False

# HSV Color Thresholds for Line Detection
HSV_YELLOW_LOWER = (20, 100, 100)
HSV_YELLOW_UPPER = (30, 255, 255)
HSV_WHITE_LOWER = (0, 0, 200)
HSV_WHITE_UPPER = (180, 25, 255)

GPIO_CONFIG = {
    'STEER_PIN': 12,
    'THROTTLE_PIN': 13
}

PWM_CONFIG = {
    'FREQUENCY': 50,  # 通用频率
    'RANGE': 1000     # 比较高的精度
}

SPEED_CONFIG = {
    'NEUTRAL_DUTY': 75,      # 1.5ms 相当于 75/1000 占空比（50Hz 时）
    'CENTER_DUTY': 53.5,     # 1.07ms 转向中位
    'MAX_DUTY_DIFF': 17      # 0.34ms = 最大偏移量（17/1000）
}



# PID Controller Parameters
KP = 0.1  # Proportional gain
KI = 0.01  # Integral gain
KD = 0.05  # Derivative gain
SETPOINT = 320  # Center point for line following


# Image Processing
ROI_HEIGHT = 100  # Height of region of interest
ROI_OFFSET = 100  # Offset from bottom of frame
BLUR_KERNEL_SIZE = (5, 5)
MIN_CONTOUR_AREA = 500
