import sys
import time
sys.path.append('..')  # 添加父目录到路径

from control.vehicle_control import VehicleController

def test_basic_movements():
    print("开始测试基本动作...")
    
    # 初始化车辆控制器
    try:
        car = VehicleController()
        car.steering_center()
        print('drive_forward')
        car.drive_forward()           # 前进80%
        time.sleep(2)

        print('drive_neutral')
        car.drive_neutral()
        time.sleep(2)

        print('drive_backward')
        car.drive_backward()
        time.sleep(2)

        # print("✅ 转向测试开始...")
        # time.sleep(1)

        # # 中间位置
        # print("🎯 回正方向")
        # car.steering_center()
        # time.sleep(1)

        # # 小角度右转
        # print("➡️ 右转 30%")
        # car.adjust_steering('right', 10)
        # time.sleep(1)

        # # 中角度右转
        # print("➡️ 右转 60%")
        # car.adjust_steering('right', 30)
        # time.sleep(1)

        # # 最大角度右转
        # print("➡️ 右转 100%")
        # car.adjust_steering('right', 60)
        # time.sleep(1)

        # # 回中
        # print("🎯 回正方向")
        # car.steering_center()
        # time.sleep(1)

        # # 小角度左转
        # print("⬅️ 左转 30%")
        # car.adjust_steering('left', 10)
        # time.sleep(1)

        # # 中角度左转
        # print("⬅️ 左转 60%")
        # car.adjust_steering('left', 30)
        # time.sleep(1)

        # # 最大角度左转
        # print("⬅️ 左转 100%")
        # car.adjust_steering('left', 60)
        # time.sleep(1)

        # # 最后回正
        # print("🎯 回正方向")
        # car.steering_center()
        # time.sleep(1)

        # # 停止所有 PWM 输出（保险）
        # print("🛑 停止所有 PWM 信号")
        # car.stop()
        # print("✅ 测试结束")
        
        # # 测试左转
        # print("测试左转 2 秒...")
        # vehicle.drive_forward(speed=40)
        # vehicle.adjust_steering(-30)
        # time.sleep(2)
        # vehicle.stop()
        # time.sleep(1)
        
        # # 测试右转
        # print("测试右转 2 秒...")
        # vehicle.drive_forward(speed=40)
        # vehicle.adjust_steering(30)
        # time.sleep(2)
        # vehicle.stop()
        # time.sleep(1)
        
        # # 测试不同速度
        # print("测试不同速度变化...")
        # speeds = [30, 50, 70]
        # for speed in speeds:
        #     print(f"测试速度 {speed}%...")
        #     vehicle.drive_forward(speed=speed)
        #     time.sleep(2)
        
        # 最后停止
        print("测试完成，停止车辆")
        car.stop()
        
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        if 'vehicle' in locals():
            car.stop()
    
if __name__ == "__main__":
    test_basic_movements()
