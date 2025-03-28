import unittest
import time
from logic.decision import DecisionMaker, VehicleState

class TestDecisionMaker(unittest.TestCase):
    def setUp(self):
        self.decision_maker = DecisionMaker()

    def test_normal_driving(self):
        """测试正常行驶情况"""
        decision = self.decision_maker.make_decision(lane_data=10, sign_data=None, light_data='green')
        self.assertEqual(decision['action'], 'forward')
        self.assertEqual(decision['steering'], 10)
        self.assertEqual(self.decision_maker.current_state, VehicleState.NORMAL)

    def test_stop_sign_behavior(self):
        """测试停止标志行为"""
        # 初次遇到停止标志
        decision = self.decision_maker.make_decision(lane_data=0, sign_data='stop', light_data='green')
        self.assertEqual(decision['action'], 'stop')
        self.assertEqual(self.decision_maker.current_state, VehicleState.STOPPED)

        # 等待不到3秒
        time.sleep(1)
        decision = self.decision_maker.make_decision(lane_data=0, sign_data='stop', light_data='green')
        self.assertEqual(decision['action'], 'stop')

        # 等待超过3秒
        time.sleep(2.1)  # 总共等待超过3秒
        decision = self.decision_maker.make_decision(lane_data=5, sign_data='stop', light_data='green')
        self.assertEqual(decision['action'], 'forward')
        self.assertEqual(self.decision_maker.current_state, VehicleState.NORMAL)

    def test_turn_signs(self):
        """测试转向标志"""
        # 测试右转
        decision = self.decision_maker.make_decision(lane_data=0, sign_data='right', light_data='green')
        self.assertEqual(decision['action'], 'turn')
        self.assertEqual(decision['steering'], 45)
        self.assertEqual(self.decision_maker.current_state, VehicleState.TURNING)

        # 测试左转
        decision = self.decision_maker.make_decision(lane_data=0, sign_data='left', light_data='green')
        self.assertEqual(decision['action'], 'turn')
        self.assertEqual(decision['steering'], -45)
        self.assertEqual(self.decision_maker.current_state, VehicleState.TURNING)

    def test_traffic_lights(self):
        """测试红绿灯行为"""
        # 测试红灯
        decision = self.decision_maker.make_decision(lane_data=0, sign_data=None, light_data='red')
        self.assertEqual(decision['action'], 'stop')
        self.assertEqual(self.decision_maker.current_state, VehicleState.STOPPED)

        # 测试黄灯
        decision = self.decision_maker.make_decision(lane_data=0, sign_data=None, light_data='yellow')
        self.assertEqual(decision['action'], 'stop')
        self.assertEqual(self.decision_maker.current_state, VehicleState.STOPPED)

if __name__ == '__main__':
    unittest.main()
