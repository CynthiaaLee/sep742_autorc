from picamera2 import Picamera2, Preview
import picamera2.encoders
from datetime import datetime
import os

class CameraStream:
    def __init__(self, resolution=(640, 480)):
        self.camera = Picamera2()
        self.camera_config = self.camera.create_video_configuration(
            main={"size": resolution, "format": "YUV420"}
        )
        self.camera.configure(self.camera_config)
        self.save_directory = os.path.expanduser("~/Videos")
        self.is_recording = False

        # Create save directory if it doesn't exist
        os.makedirs(self.save_directory, exist_ok=True)

    def start(self):
        """启动摄像头流"""
        self.camera.start()

    def stop(self):
        """停止摄像头流和录制"""
        if self.is_recording:
            self.stop_recording()
        self.camera.stop()

    def capture_frame(self):
        """捕获单帧"""
        try:
            return self.camera.capture_array()
        except Exception as e:
            print(f"Frame capture error: {e}")
            return None

    def generate_filename(self):
        """生成基于时间戳的文件名"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(self.save_directory, f"recording_{timestamp}.h264")

    def start_recording(self, output_file=None):
        """开始录制视频"""
        if output_file is None:
            output_file = self.generate_filename()
        print(f"Starting recording: {output_file}")
        self.encoder = picamera2.encoders.H264Encoder()
        self.camera.start_recording(self.encoder, output_file)
        self.is_recording = True

    def stop_recording(self):
        """停止录制视频"""
        if self.is_recording:
            print("Stopping recording")
            self.camera.stop_recording()
            self.is_recording = False

# # 示例用法
# if __name__ == "__main__":
#     camera = CameraStream()
#     camera.start()

#     # 捕获一帧
#     frame = camera.capture_frame()
#     if frame is not None:
#         print("Frame captured successfully")

#     # 开始录制
#     camera.start_recording()
    
#     # 停止录制
#     camera.stop_recording()

#     camera.stop()