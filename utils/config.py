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
    # 'FORWARD_MS': 1.15,
    # 'BACKWARD_MS': 1.65,
    'FORWARD_MS': 1.32,
    'BACKWARD_MS': 1.64,
}

STEERING_CONFIG = {
    'CENTER_DUTY': 53.5,
    'MAX_DUTY_DIFF': 11
}

MIN_STOP_SIGN_WIDTH = 130  # 根据你图像分辨率调整这个阈值