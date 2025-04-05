import time

from control.vehicle_control import VehicleController


def test_throttle():
    print("Start testing throttle...")
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
        print("\n🛑 Detected KeyboardInterrupt, safely exiting the program.")
    except Exception as e:
        print(f"❌ An error occurred during the test: {str(e)}")

def test_steering():
    print("Start testing steering...")

    try:
        with VehicleController() as car:
            time.sleep(2)
            car.drive_neutral()
            car.steering_center()
            time.sleep(1)

            while True:
                print("✅ Steering test begins...")
                time.sleep(1)

                # Center position
                print("🎯 Reset to center")
                car.steering_center()
                time.sleep(1)

                # Small right turn
                print("➡️ Turn right 30%")
                car.adjust_steering('right', 30)
                time.sleep(1)

                # Medium right turn
                print("➡️ Turn right 60%")
                car.adjust_steering('right', 60)
                time.sleep(1)

                # Maximum right turn
                print("➡️ Turn right 100%")
                car.adjust_steering('right', 100)
                time.sleep(1)

                # Back to center
                print("🎯 Reset to center")
                car.steering_center()
                time.sleep(1)

                # Small left turn
                print("⬅️ Turn left 30%")
                car.adjust_steering('left', 30)
                time.sleep(1)

                # Medium left turn
                print("⬅️ Turn left 60%")
                car.adjust_steering('left', 60)
                time.sleep(1)

                # Maximum left turn
                print("⬅️ Turn left 100%")
                car.adjust_steering('left', 100)
                time.sleep(1)

                # Finally back to center
                print("🎯 Reset to center")
                car.steering_center()
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Detected KeyboardInterrupt, safely exiting the program.")

    except Exception as e:
        print(f"❌ An error occurred during the test: {str(e)}")

if __name__ == "__main__":
    test_throttle()
    # test_steering()
