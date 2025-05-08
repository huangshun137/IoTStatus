import threading
import time
import json

from common import config, IOTconfig
from common.IOTconfig import TopicType
from util import MQTT_util
from util.HttpUtil import *

import urllib.parse

class MqttPublisher:
    def __init__(self):
        """
        :param gripper_state: 夹爪状态
        :param arm_state: 机械臂状态
        :param arm_instance: 机械臂实例
        :param lift_state: 升降机构状态
        :param water_info: 底盘信息
        :param water_instance: 底盘实例
        """
        self.gripper_state = None
        # self.arm_state = None
        self.arm_state = None
        self.arm_instance = None
        self.lift_state = None
        self.water_info = None
        self.water_instance = None
        self.servo_state = None
        self.camera_state = None
        self.iot_water = IOTconfig.DeviceTopic(config.iot_water)
        self.iot_left_gripper = IOTconfig.DeviceTopic(config.iot_left_gripper)
        self.iot_right_gripper = IOTconfig.DeviceTopic(config.iot_right_gripper)
        self.iot_lift = IOTconfig.DeviceTopic(config.iot_lift)
        self.iot_servo = IOTconfig.DeviceTopic(config.iot_servo)
        self.iot_left_arm = IOTconfig.DeviceTopic(config.iot_left_arm)
        self.iot_right_arm = IOTconfig.DeviceTopic(config.iot_right_arm)
        self.iot_camera = IOTconfig.DeviceTopic(config.iot_camera)
        self.mqtt_client = MQTT_util.MQTTClient(config.iot_address, config.iot_port)

        self.mqtt_client.on_message = self.on_message
        self.httpTool = HttpTool()

    def updateStates(self, left_arm=None, right_arm=None, water=None, servo=None, camera=None):
        """
        更新状态
        :param arm: 机械臂、夹爪、升降机构
        :param water: 底盘
        :return:
        """
        last_camera_time = time.time() - 4 # 初始化为4秒前，确保第一次循环立即执行
        while True:
            current_time = time.time()  # 获取当前时间
            time.sleep(2)
            if left_arm is not None:
                # self.gripper_state = left_arm.check_arm_state()
                # arm_state = left_arm.check_arm_state()
                self.arm_state = left_arm.check_arm_state()
                self.arm_instance = left_arm
                self.lift_state = left_arm.check_lift_state()
            if right_arm is not None:
                self.gripper_state = right_arm.check_arm_state()
                self.arm_state = right_arm.check_gripper_state()
            if water is not None:
                self.water_instance = water
                robot_info = water.get_robot_status()
                robot_battery_info = water.get_robot_battery_info()
                self.water_info = {**robot_info, **robot_battery_info}
            if servo is not None:
                self.servo_state = servo.check_servo_state()
            if camera is not None:
                if current_time - last_camera_time >= 4:
                    self.camera_state = camera.check_camera_state()
                    last_camera_time = current_time  # 重置最后检查时间

    def publicState(self, time_delay=2):
        """发布状态"""
        self.mqtt_client.connect()
        while True:
            if self.mqtt_client.is_connected():
                self.subscribeMqtt()
                break
        while True:
            if self.mqtt_client.is_connected():
                # self.publicRightGripper()
                # self.publicLeftGripper()
                self.publicLeftArm()
                # self.publicRightArm()
                # self.publicLift()
                self.publicWater()
                self.publicCamera()
                time.sleep(time_delay)

    def publicServo(self):
        """发布状态"""
        topic = self.iot_lift.get_topic(TopicType.DEVICE_MESSAGE_UP)
        mesg = self.lift_state
        self.mqtt_client.publish(topic, mesg)

    def publicLift(self):
        """发布状态"""
        topic = self.iot_lift.get_topic(TopicType.DEVICE_MESSAGE_UP)
        mesg = self.lift_state
        self.mqtt_client.publish(topic, mesg)

    def publicLeftGripper(self):
        """发布状态"""
        topic = self.iot_left_gripper.get_topic(TopicType.DEVICE_MESSAGE_UP)
        mesg = self.gripper_state
        self.mqtt_client.publish(topic, mesg)

    def publicRightGripper(self):
        """发布状态"""
        topic = self.iot_right_gripper.get_topic(TopicType.DEVICE_MESSAGE_UP)
        mesg = self.gripper_state
        self.mqtt_client.publish(topic, mesg)

    def publicLeftArm(self):
        """发布状态"""
        if not self.arm_state or not self.lift_state:
            return
        topic = self.iot_left_arm.get_topic(TopicType.DEVICE_MESSAGE_UP)
        mesg = { "isOnline": True }
        self.mqtt_client.publish(topic, mesg)

        topic = self.iot_left_arm.get_topic(TopicType.DEVICE_PROPERTIES_REPORT)
        mesg = {
            "lift_pos": self.lift_state.get("height", None),
            "lift_mode": self.lift_state.get("mode", None),
            "arm_joint": self.arm_state.get("joint", None),
            "arm_pose": self.arm_state.get("pose", None),
        }
        self.mqtt_client.publish(topic, mesg)

    def publicRightArm(self):
        """发布状态"""
        topic = self.iot_right_arm.get_topic(TopicType.DEVICE_MESSAGE_UP)
        mesg = self.arm_state
        self.mqtt_client.publish(topic, mesg)

    def publicWater(self):
        """发布状态"""
        if (self.water_info is None):
            return
        topic = self.iot_water.get_topic(TopicType.DEVICE_MESSAGE_UP)
        mesg = { "isOnline": True }
        self.mqtt_client.publish(topic, mesg)

        topic = self.iot_water.get_topic(TopicType.DEVICE_PROPERTIES_REPORT)
        mesg = {
            "move_target": self.water_info.get("move_target", None),
            "move_status": self.water_info.get("move_status", None),
            "charge_state": self.water_info.get("charge_state", None),
            "soft_estop_state": self.water_info.get("soft_estop_state", None),
            "hard_estop_state": self.water_info.get("hard_estop_state", None),
            "power_percent": self.water_info.get("power_percent", None),
            "battery_current": self.water_info.get("battery_current", None),
            "head_current": self.water_info.get("head_current", None),
            "current_pose": self.water_info.get("current_pose", None),
        }
        self.mqtt_client.publish(topic, mesg)

    def publicCamera(self):
        """发布状态"""
        if (self.camera_state is None or not self.camera_state["image_base64"]):
            return
        topic = self.iot_camera.get_topic(TopicType.DEVICE_MESSAGE_UP)
        mesg = { "isOnline": True }
        self.mqtt_client.publish(topic, mesg)

    def subscribeWaterMqtt(self):
        """订阅MQTT"""
        commandTopic = self.iot_water.get_topic(TopicType.DEVICE_COMMAND_REQUEST)
        self.mqtt_client.subscribe(commandTopic)
        propertyTopic = self.iot_water.get_topic(TopicType.DEVICE_PROPERTIES_SET_REQUEST)
        self.mqtt_client.subscribe(propertyTopic)
        
    def subscribeArmMqtt(self):
        """订阅MQTT"""
        commandTopic = self.iot_left_arm.get_topic(TopicType.DEVICE_COMMAND_REQUEST)
        self.mqtt_client.subscribe(commandTopic)
        propertyTopic = self.iot_left_arm.get_topic(TopicType.DEVICE_PROPERTIES_SET_REQUEST)
        self.mqtt_client.subscribe(propertyTopic)

    def subscribeMqtt(self):
        """订阅MQTT"""
        self.subscribeWaterMqtt()
        self.subscribeArmMqtt()

    def on_message(self, client, userdata, msg):
        """接收MQTT消息"""
        print("--------------MQTT信息:", msg.topic, msg.payload)
        if ("/sys/commands" in msg.topic or "/sys/properties/set" in msg.topic) and "response" not in msg.topic:
            # 处理命令下发请求
            _device_id = msg.topic.split("/")[2]
            request_id = msg.topic.split("/")[-1].split("=")[1]
            params = json.loads(msg.payload.decode())
            print(f"收到请求ID: {request_id}，请求参数: {params}")
            request_url = params.get("requestUrl", None)
            request_method = params.get("requestMethod", None)
            if not request_url:
                # 判断是否有请求方法
                if request_method:
                    # 具体到各自controller中匹配对应的方法名，执行对应的请求
                    if _device_id == config.iot_left_arm:
                        # 机械臂请求
                        if hasattr(self.arm_instance, request_method):
                            method = getattr(self.arm_instance, request_method)
                            response = method(params)
                        else:
                            response = {
                                "ok": False,
                                "msg": f"未找到方法: {request_method}"
                            }
                else:
                    response = {
                        "ok": False,
                        "msg": "未设置请求方法，请求失败"
                    }
            else:
                # 发请求
                del params['requestUrl']
                query_string = urllib.parse.urlencode(params).replace("True", "true").replace("False", "false")
                # print(query_string)
                _request_url = f"{request_url}?{query_string}"
                res = self.httpTool.get(_request_url)
                print(res)
                response = {
                    "ok": res["status"] == "OK",
                    "msg": res.get("error_message", ""),
                }
            # mqtt返回消息
            commandResTopic = f"/devices/{_device_id}/sys/commands/response/request_id={request_id}"
            propertyResTopic = f"/devices/{_device_id}/sys/properties/set/response/request_id={request_id}"
            _topic = commandResTopic if "/sys/commands" in msg.topic else propertyResTopic
            self.mqtt_client.publish(_topic, response)



# 使用示例
# if __name__ == "__main__":
#     publisher = MqttPublisher()

#     # 创建并启动发布状态的线程
#     update_thread1 = threading.Thread(target=publisher.publicState)

#     update_thread1.start()
