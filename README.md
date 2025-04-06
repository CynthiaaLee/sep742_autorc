# Autonomous RC Car Project

A Python-based autonomous RC car system that uses computer vision and real-time control to navigate based on lane detection, traffic signs, and traffic lights.

## Requirements

### Hardware
- Raspberry Pi (3 or newer)
- Pi Camera Module
- RC Car with servo control capability 
- Servo controller board

### Software Dependencies
- Python 3.7+
- OpenCV 4.x
- pigpio
- NumPy

Install dependencies:
```bash
pip install requirements.txt
```

On Raspberry Pi, also run:
```bash
sudo apt-get update
sudo apt-get install pigpiod
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

## Project Structure

```
sep742_autorc/
├── camera/           # Camera handling and video stream
├── control/          # Vehicle control logic
├── logic/           # Decision making and perception memory
├── models/          # Pre-trained detection models
├── perception/      # Computer vision algorithms
├── utils/           # Configuration and utilities
└── main.py         # Main application entry point
```

### Key Components

- **Camera Stream**: Handles video input from Pi camera or test videos
- **Vehicle Control**: Manages RC car steering and throttle
- **Perception**: 
  - Lane detection
  - Traffic sign detection (Stop signs)
  - Traffic light detection
- **Decision Making**: Processes perception data to control vehicle
- **Configuration**: System parameters in utils/config.py

## Usage

### Basic Execution
```bash
python main.py
```

### Debug Mode with Video Input
```python
video_path = "models/test_video.mp4"  # Optional: Use video file instead of camera
run(debug=True, video_path=video_path)
```

## Configuration

Key settings in `utils/config.py`:
- Camera resolution and frame rate
- GPIO pins for steering and throttle
- PWM parameters
- Vehicle control parameters
- Detection thresholds

## Features

1. **Lane Following**
   - Real-time lane detection
   - Steering angle calculation
   - Smooth trajectory control

2. **Traffic Sign Detection**
   - Stop sign recognition
   - Distance-based response
   - State tracking for reliable detection

3. **Traffic Light Detection**
   - Color-based light state detection
   - State tracking for reliable detection

4. **Autonomous Decision Making**
   - Real-time processing of sensor data
   - Multi-factor decision making
   - Safe stop and go behaviors

## Output

- Debug visualization available in debug mode
- Video recording of autonomous operation
- Logging of system events and decisions

## Safety Features

- Automatic stop on sign detection
- Fail-safe shutdown on errors
- State tracking to prevent false detections
- Emergency stop capability

## Development

The system is modular and extensible. Key areas for potential enhancement:
- Additional traffic sign recognition
- Advanced path planning
- Speed control optimization
- Enhanced obstacle detection

## Troubleshooting

1. **Camera Issues**
   - Ensure camera is properly connected
   - Check camera permissions
   - Verify resolution settings

2. **Control Issues**
   - Verify pigpiod is running
   - Check GPIO pin configurations
   - Validate PWM settings

3. **Detection Issues**
   - Verify model files are present
   - Check camera image quality
   - Adjust detection thresholds

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License.
