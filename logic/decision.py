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
        self.waiting_for_stop_to_complete = False  # 增加此状态标志

    def make_decision(self, lane_data, is_stop_sign, light_data):
        # 如果之前触发了stop sign逻辑，就持续等待3秒
        if self.waiting_for_stop_to_complete:
            if time.time() - self.stop_start_time >= 3:
                print("Stop sign duration exceeded 3 seconds, proceeding.")
                self.waiting_for_stop_to_complete = False
                self.current_state = VehicleState.NORMAL
                steering = lane_data if lane_data is not None else self.last_steering
                self.last_steering = steering
                return self._build_decision('forward', steering)
            print("Still waiting for stop sign duration to complete.")
            self.current_state = VehicleState.STOPPED
            return self._build_decision('stop', 0)

        # 检测到新的 stop sign，开始等待流程
        if is_stop_sign or light_data in ['red', 'yellow']:
            self.stop_start_time = time.time()
            self.waiting_for_stop_to_complete = True
            self.current_state = VehicleState.STOPPED
            print("Stop sign detected, initiating stop.")
            return self._build_decision('stop', 0)

        # # 红灯或黄灯
        # if light_data in ['red', 'yellow']:
        #     self.current_state = VehicleState.STOPPED
        #     return self._build_decision('stop', 0)

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
        strength = int((min(abs(angle), 45) / 45) * 160)
        return direction, strength
