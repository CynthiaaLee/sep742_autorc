import sys
import os
import time

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from camera.camera_stream import CameraStream

def test_camera_stream():
    with CameraStream(resolution=(640, 480)) as camera:
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
