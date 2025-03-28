# Configuration parameters for autonomous RC car

# Camera Settings
CAMERA_RESOLUTION = (640, 480)
FRAME_RATE = 30

GPIO_CONFIG = {
    'STEER_PIN': 12,
    'THROTTLE_PIN': 13
}

PWM_CONFIG = {
    'FREQUENCY': 50,  # 通用频率
    'RANGE': 1000     # 比较高的精度
}

SPEED_CONFIG = {
    'NEUTRAL_MS': 1.5,
    # 'FORWARD_MS': 1.32,
    # 'BACKWARD_MS': 1.60,
    'FORWARD_MS': 1.32,
    'BACKWARD_MS': 1.64,
    # 'FORWARD_MS': 1.2,
    # 'BACKWARD_MS': 1.60,
}

STEERING_CONFIG = {
    'CENTER_DUTY': 53.5,
    'MAX_DUTY_DIFF': 11
}

# # Image Processing
# ROI_HEIGHT = 100  # Height of region of interest
# ROI_OFFSET = 100  # Offset from bottom of frame
# BLUR_KERNEL_SIZE = (5, 5)
# MIN_CONTOUR_AREA = 500
