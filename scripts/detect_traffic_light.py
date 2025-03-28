from perception.traffic_light_detection import TrafficLightDetector
import sys

def main():
    # 初始化检测器
    detector = TrafficLightDetector()
    
    # 获取输入图片路径
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = 'https://sanjosespotlight.s3.us-east-2.amazonaws.com/wp-content/uploads/2023/05/19153716/IMG_9313-scaled.jpg'
    
    # 处理图片
    color, bbox = detector.process_image(
        image_path,
        save_path='results_traffic_light.jpg'
    )
    
    if color:
        print(f"检测到{color}灯")
        print(f"位置: {bbox}")
    else:
        print("未检测到交通灯")

if __name__ == '__main__':
    main()
