import pigpio
from utils.config import GPIO_CONFIG, PWM_CONFIG, SPEED_CONFIG

class VehicleController:
    def __init__(self):
        self.STEER_PIN = GPIO_CONFIG['STEER_PIN']
        self.THROTTLE_PIN = GPIO_CONFIG['THROTTLE_PIN']

        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpio daemon not connected.")

        self.setup_gpio()

    def setup_gpio(self):
        for pin in [self.STEER_PIN, self.THROTTLE_PIN]:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.set_PWM_frequency(pin, PWM_CONFIG['FREQUENCY'])
            self.pi.set_PWM_range(pin, PWM_CONFIG['RANGE'])

    # def set_throttle_percent(self, percent):
    #     """控制油门，percent: -100（倒车）到 +100（前进）"""
    #     percent = max(-100, min(percent, 100))
    #     mid = SPEED_CONFIG['NEUTRAL_DUTY']
    #     diff = SPEED_CONFIG['MAX_DUTY_DIFF']
    #     duty = mid + int(diff * (percent / 100))
    #     print(f"Pin: {self.THROTTLE_PIN}, Throttle: {duty}")
    #     self.pi.set_PWM_dutycycle(self.THROTTLE_PIN, duty)

    def set_steering_percent(self, percent):
        """控制转向，percent: -100（左）到 +100（右）"""
        percent = max(-100, min(percent, 100))
        mid = SPEED_CONFIG['CENTER_DUTY']
        diff = SPEED_CONFIG['MAX_DUTY_DIFF']
        duty = mid + int(diff * (percent / 100))
        print(f"Pin: {self.STEER_PIN}, Throttle: {duty}")
        # self.pi.set_PWM_dutycycle(self.STEER_PIN, duty)

    # def drive_forward(self, speed=100):
    #     self.set_throttle_percent(speed)

    # def drive_backward(self, speed=100):
    #     self.set_throttle_percent(-speed)

    # def drive_neutral(self):
    #     self.set_throttle_percent(0)
    
    def drive_forward(self, speed=None):
        # 1.5ms ~ 2.0ms 数值越大，速度越快
        ms = SPEED_CONFIG.get('FORWARD_MS', 1.5)
        self.set_throttle_ms(ms)

    def drive_backward(self, speed=None):
        # 1.0ms ~ 1.5ms 数值越小，速度越快
        ms = SPEED_CONFIG.get('REVERSE_MS', 1.1)
        self.set_throttle_ms(ms)

    def drive_neutral(self):
        self.set_throttle_ms(SPEED_CONFIG.get('NEUTRAL_MS', 1.5))

    def set_throttle_ms(self, ms):
        period_ms = 1000 / PWM_CONFIG['FREQUENCY']
        duty_ratio = ms / period_ms
        pwm_value = int(duty_ratio * PWM_CONFIG['RANGE'])
        print(f"Pin: {GPIO_CONFIG['THROTTLE_PIN']}, Throttle: {pwm_value}")
        # self.pi.set_PWM_dutycycle(GPIO_CONFIG['THROTTLE_PIN'], pwm_value)

    def adjust_steering(self, direction, strength=100):
        if direction == 'left':
            self.set_steering_percent(-strength)
        elif direction == 'right':
            self.set_steering_percent(strength)
        else:
            self.set_steering_percent(0)

    def steering_center(self):
        self.set_steering_percent(0)

    def stop(self):
        self.pi.set_PWM_dutycycle(self.STEER_PIN, 0)
        self.pi.set_PWM_dutycycle(self.THROTTLE_PIN, 0)

    def __del__(self):
        if hasattr(self, 'pi') and self.pi.connected:
            self.stop()
            self.pi.stop()
