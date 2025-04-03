import time
from camera.camera_stream import CameraStream

def test_camera_stream():
    with CameraStream() as camera:
        print("Camera started, beginning recording test...")

        try:
            # Start recording
            camera.start_recording()
            print("Recording started. Press Ctrl+C to stop...")

            # Keep recording until interrupted
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Stopping recording...")

        except Exception as e:
            print(f"Error during recording: {str(e)}")

        finally:
            camera.stop_recording()
            print("Recording stopped.")

if __name__ == "__main__":
    test_camera_stream()
