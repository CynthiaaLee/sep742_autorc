import subprocess
import time

import pigpio

from utils.config import GPIO_CONFIG, PWM_CONFIG, SPEED_CONFIG, STEERING_CONFIG

print(SPEED_CONFIG)
print(STEERING_CONFIG)

def ensure_pigpiod_running():
    try:
        result = subprocess.run(['pgrep', 'pigpiod'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("[INFO] pigpiod is not running. Starting it now...")
            subprocess.run(['sudo', 'pigpiod'], check=True)
            time.sleep(0.5)
        else:
            print("[INFO] pigpiod is already running.")

        pi = pigpio.pi()
        if not pi.connected:
            raise RuntimeError("Unable to connect to pigpiod after starting it.")
        pi.stop()
    except Exception as e:
        raise RuntimeError(f"Error ensuring pigpiod is running: {e}")


class VehicleController:
    def __init__(self):
        ensure_pigpiod_running()
        self.STEER_PIN = GPIO_CONFIG['STEER_PIN']
        self.THROTTLE_PIN = GPIO_CONFIG['THROTTLE_PIN']
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpio daemon not connected.")

        self.setup_gpio()
        self.steering_center()
        self.drive_neutral()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        if self.pi.connected:
            self.pi.stop()

    def setup_gpio(self):
        for pin in [self.STEER_PIN, self.THROTTLE_PIN]:
            self.pi.set_PWM_frequency(pin, PWM_CONFIG['FREQUENCY'])
            self.pi.set_PWM_range(pin, PWM_CONFIG['RANGE'])

    def set_steering_percent(self, percent):
        """Control steering, percent: -100 (left) to +100 (right)"""
        percent = max(-100, min(percent, 100))
        mid = STEERING_CONFIG['CENTER_DUTY']
        diff = STEERING_CONFIG['MAX_DUTY_DIFF']
        duty = mid + int(diff * (percent / 100))
        print(f"Pin: {self.STEER_PIN}, Throttle: {duty}")
        self.pi.set_PWM_dutycycle(self.STEER_PIN, duty)
    
    def drive_forward(self):
        ms = SPEED_CONFIG['FORWARD_MS']
        self.set_throttle_ms(ms)

    def drive_backward(self):
        ms = SPEED_CONFIG['BACKWARD_MS']
        self.set_throttle_ms(ms)

    def drive_neutral(self):
        self.set_throttle_ms(SPEED_CONFIG['NEUTRAL_MS'])

    def set_throttle_ms(self, ms):
        period_ms = 1000 / PWM_CONFIG['FREQUENCY']
        duty_ratio = ms / period_ms
        pwm_value = duty_ratio * PWM_CONFIG['RANGE']
        # pwm_value: backward: 81, forward: 66, neutral: 75.
        print(f"Pin: {GPIO_CONFIG['THROTTLE_PIN']}, Throttle: {pwm_value}")
        self.pi.set_PWM_dutycycle(GPIO_CONFIG['THROTTLE_PIN'], pwm_value)

    def adjust_steering(self, direction, strength=100):
        if direction == 'left':
            self.set_steering_percent(-strength)
        elif direction == 'right':
            self.set_steering_percent(strength)
        else:
            self.steering_center()

    def steering_center(self):
        self.set_steering_percent(0)

    def stop(self):
        self.pi.set_PWM_dutycycle(self.STEER_PIN, 0)
        self.pi.set_PWM_dutycycle(self.THROTTLE_PIN, 0)