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
                # 第一次检测到 stop sign，记录停止时间
                self.stop_start_time = time.time()
                self.current_state = VehicleState.STOPPED
                return {'action': 'stop', 'steering': 0}
            
            # 检查是否已经停了三秒
            if time.time() - self.stop_start_time >= 3:
                self.current_state = VehicleState.NORMAL  # 恢复正常状态
                # 返回前进的动作
                steering = lane_data if lane_data is not None else self.last_steering
                self.last_steering = steering
                return {'action': 'forward', 'steering': steering}
            
            # 如果未满三秒，继续保持停止状态
            return {'action': 'stop', 'steering': 0}

        # 遇到红灯或黄灯
        if light_data in ['red', 'yellow']:
            self.current_state = VehicleState.STOPPED
            return {'action': 'stop', 'steering': 0}
            
        # 遇到左转或右转标志
        if sign_data in ['left', 'right']:
            self.current_state = VehicleState.TURNING
            return {'action': 'turn', 'steering': 45 if sign_data == 'right' else -45}
            
        # 正常行驶
        self.current_state = VehicleState.NORMAL
        # 平滑转向
        steering = lane_data if lane_data is not None else self.last_steering
        self.last_steering = steering
        return {'action': 'forward', 'steering': steering}