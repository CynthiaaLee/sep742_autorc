import sys
import time

from control.vehicle_control import VehicleController

def test_throttle():
    print("开始测试油门...")
    try:
        with VehicleController() as car:
            time.sleep(5)
            car.drive_neutral()
            car.steering_center()
            time.sleep(1)
            while True:

                print('-------------------')

                print('drive_neutral')
                car.drive_neutral()
                time.sleep(5)

                print('drive_forward')
                car.drive_forward()
                time.sleep(2)

                # print('drive_neutral')
                # car.drive_neutral()
                # time.sleep(5)
                # car.stop()

                # print('drive_backward')
                # car.drive_backward()
                # time.sleep(2)
                
    except KeyboardInterrupt:
        print("\n🛑 检测到 KeyboardInterrupt，已安全退出程序。")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")

def test_steering():
    print("开始测试转向...")

    try:
        with VehicleController() as car:
            time.sleep(2)
            car.drive_neutral()
            car.steering_center()
            time.sleep(1)

            while True:
                print("✅ 转向测试开始...")
                time.sleep(1)

                # 中间位置
                print("🎯 回正方向")
                car.steering_center()
                time.sleep(1)

                # 小角度右转
                print("➡️ 右转 30%")
                car.adjust_steering('right', 30)
                time.sleep(1)

                # 中角度右转
                print("➡️ 右转 60%")
                car.adjust_steering('right', 60)
                time.sleep(1)

                # 最大角度右转
                print("➡️ 右转 100%")
                car.adjust_steering('right', 100)
                time.sleep(1)

                # 回中
                print("🎯 回正方向")
                car.steering_center()
                time.sleep(1)

                # 小角度左转
                print("⬅️ 左转 30%")
                car.adjust_steering('left', 30)
                time.sleep(1)

                # 中角度左转
                print("⬅️ 左转 60%")
                car.adjust_steering('left', 60)
                time.sleep(1)

                # 最大角度左转
                print("⬅️ 左转 100%")
                car.adjust_steering('left', 100)
                time.sleep(1)

                # 最后回正
                print("🎯 回正方向")
                car.steering_center()
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 检测到 KeyboardInterrupt，已安全退出程序。")

    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    test_throttle()
    # test_steering()
