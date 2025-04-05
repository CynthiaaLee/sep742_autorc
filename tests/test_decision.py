import time
import unittest

from logic.decision import DecisionMaker, VehicleState


class TestDecisionMaker(unittest.TestCase):
    def setUp(self):
        self.decision_maker = DecisionMaker()

    def test_normal_driving(self):
        """Test normal driving conditions"""
        decision = self.decision_maker.make_decision(lane_data=10, sign_data=None, light_data='green')
        self.assertEqual(decision['action'], 'forward')
        self.assertEqual(decision['steering'], 10)
        self.assertEqual(self.decision_maker.current_state, VehicleState.NORMAL)

    def test_stop_sign_behavior(self):
        """Test stop sign behavior"""
        # First encounter with a stop sign
        decision = self.decision_maker.make_decision(lane_data=0, sign_data='stop', light_data='green')
        self.assertEqual(decision['action'], 'stop')
        self.assertEqual(self.decision_maker.current_state, VehicleState.STOPPED)

        # Wait less than 3 seconds
        time.sleep(1)
        decision = self.decision_maker.make_decision(lane_data=0, sign_data='stop', light_data='green')
        self.assertEqual(decision['action'], 'stop')

        # Wait more than 3 seconds
        time.sleep(2.1)  # Total wait time exceeds 3 seconds
        decision = self.decision_maker.make_decision(lane_data=5, sign_data='stop', light_data='green')
        self.assertEqual(decision['action'], 'forward')
        self.assertEqual(self.decision_maker.current_state, VehicleState.NORMAL)

    def test_turn_signs(self):
        """Test turn signs"""
        # Test right turn
        decision = self.decision_maker.make_decision(lane_data=0, sign_data='right', light_data='green')
        self.assertEqual(decision['action'], 'turn')
        self.assertEqual(decision['steering'], 45)
        self.assertEqual(self.decision_maker.current_state, VehicleState.TURNING)

        # Test left turn
        decision = self.decision_maker.make_decision(lane_data=0, sign_data='left', light_data='green')
        self.assertEqual(decision['action'], 'turn')
        self.assertEqual(decision['steering'], -45)
        self.assertEqual(self.decision_maker.current_state, VehicleState.TURNING)

    def test_traffic_lights(self):
        """Test traffic light behavior"""
        # Test red light
        decision = self.decision_maker.make_decision(lane_data=0, sign_data=None, light_data='red')
        self.assertEqual(decision['action'], 'stop')
        self.assertEqual(self.decision_maker.current_state, VehicleState.STOPPED)

        # Test yellow light
        decision = self.decision_maker.make_decision(lane_data=0, sign_data=None, light_data='yellow')
        self.assertEqual(decision['action'], 'stop')
        self.assertEqual(self.decision_maker.current_state, VehicleState.STOPPED)

if __name__ == '__main__':
    unittest.main()
