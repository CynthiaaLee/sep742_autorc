from enum import Enum
import time

class VehicleState(Enum):
    NORMAL = "normal"
    STOPPED = "stopped"
    TURNING = "turning"
    DESTINATION = "destination"

class DecisionMaker:
    def __init__(self):
        self.current_state = VehicleState.NORMAL
        self.last_steering = 0
        self.stop_start_time = None  # 用于记录 stop sign 停止的开始时间
        
    def make_decision(self, lane_data, sign_data, light_data):
        # 遇到 stop sign
        if sign_data == 'stop':
            if self.current_state != VehicleState.STOPPED:
                self.stop_start_time = time.time()
                self.current_state = VehicleState.STOPPED
                return self._build_decision('stop', 0)
            
            if time.time() - self.stop_start_time >= 3:
                self.current_state = VehicleState.NORMAL
                steering = lane_data if lane_data is not None else self.last_steering
                self.last_steering = steering
                return self._build_decision('forward', steering)

            return self._build_decision('stop', 0)

        # 红灯或黄灯
        if light_data in ['red', 'yellow']:
            self.current_state = VehicleState.STOPPED
            return self._build_decision('stop', 0)

        # 左右转标志
        if sign_data in ['left', 'right']:
            self.current_state = VehicleState.TURNING
            steering = 45 if sign_data == 'right' else -45
            return self._build_decision('turn', steering)

        # 正常行驶
        self.current_state = VehicleState.NORMAL
        steering = lane_data if lane_data is not None else self.last_steering
        self.last_steering = steering
        return self._build_decision('forward', steering)

    def _build_decision(self, action, steering_angle):
        direction, strength = self._map_steering(steering_angle)
        return {
            'action': action,
            'steering': steering_angle,
            'direction': direction,
            'strength': strength
        }

    def _map_steering(self, angle):
        if abs(angle) < 5:
            return 'straight', 0
        direction = 'left' if angle < 0 else 'right'
        strength = int((min(abs(angle), 45) / 45) * 100)
        return direction, strength
