import time

from camera.camera_stream import CameraStream

def test_camera_stream():
    with CameraStream() as camera:
        print("Camera started, beginning recording test...")

        try:
            # Start recording
            camera.start_recording()
            print("Recording started, will record for 10 seconds...")
            time.sleep(10)  # Record for 10 seconds
            
            # Stop recording
            camera.stop_recording()
            print("Recording completed")
            exit
            
        except Exception as e:
            print(f"Error during recording: {str(e)}")

if __name__ == "__main__":
    test_camera_stream()
