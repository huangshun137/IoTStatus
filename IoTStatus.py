import threading
import time

from common import config
# from controller import ArmController, WooshController, ServoController, WaterController
from controller import ArmControllerHttp, WaterController, CameraController
from controller.UploadStatus import MqttPublisher

def main():
    
    # arm_controller = ArmController.ArmController(config.left_arm_ip, 8080, 3)
    # arm_controller = ArmControllerJson.Controller(config.left_arm_ip, config.arm_port)
    arm_controller = ArmControllerHttp.Controller(config.left_arm_ip, config.arm_http_port)
    # right_arm_controller = ArmController.ArmController(config.right_arm_ip, 8080, 3)
    # woosh = WooshController.Woosh(config.woosh_ip, config.woosh_id)
    water = WaterController.Water(config.water_ip)
    # servo = ServoController.Servo(config.servo_ip, config.servo_id)
    camera = CameraController.Camera(config.camera_ip)

    # arm_controller.create_robot_arm()
    # right_arm_controller.create_robot_arm()

    publisher = MqttPublisher()
    # 创建并启动线程
    update_thread = threading.Thread(target=publisher.updateStates, args=(arm_controller, None, water, None, camera), daemon=True)
    public_thread = threading.Thread(target=publisher.publicState, daemon=True)
    
    update_thread.start()
    public_thread.start()

    # 主线程保持运行
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        # arm_controller.delete()
        print("\n程序终止")

if __name__ == "__main__":
    main()