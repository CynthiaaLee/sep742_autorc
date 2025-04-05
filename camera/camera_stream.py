# -*- coding: utf-8 -*-
"""
@Author: Jieying Li
@Created Date: 2025-04-04 22:41:08
@Path: /camera/camera_stream.py
"""


import os
from datetime import datetime

import picamera2.encoders
from picamera2 import Picamera2


class CameraStream:
    """A class to manage camera streaming and recording using Picamera2."""
    def __init__(self, resolution=(640, 480)):
        self.camera = Picamera2()
        self.camera_config = self.camera.create_video_configuration(
            main={"size": resolution, "format": "XRGB8888"}
        )
        self.width = resolution[0]
        self.height = resolution[1]
        self.camera.configure(self.camera_config)
        self.save_directory = os.path.expanduser("~/Videos")
        self.is_recording = False

        os.makedirs(self.save_directory, exist_ok=True)

    def __enter__(self):
        self.start()
        print("Camera started")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        self.camera.start()

    def stop(self):
        if self.is_recording:
            self.stop_recording()
        self.camera.stop()

    def capture_frame(self):
        try:
            return self.camera.capture_array()
        except Exception as e:
            print(f"Frame capture error: {e}")
            return None

    def generate_filename(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(self.save_directory, f"recording_{timestamp}.h264")

    def start_recording(self, output_file=None):
        if output_file is None:
            output_file = self.generate_filename()
        print(f"Starting recording: {output_file}")
        self.encoder = picamera2.encoders.H264Encoder()
        self.camera.start_recording(self.encoder, output_file)
        self.is_recording = True

    def stop_recording(self):
        if self.is_recording:
            print("Stopping recording")
            self.camera.stop_recording()
            self.is_recording = False
