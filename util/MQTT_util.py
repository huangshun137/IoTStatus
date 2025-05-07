import paho.mqtt.client as mqtt
import json
import time
from util.log_util import default_logger as logger

class MQTTClient:
    def __init__(self, broker_address, port, keepalive=60, reconnect_delay_set=(1, 5)):
        """
        初始化MQTT客户端实例
        :param broker_address: MQTT服务器地址
        :param port: MQTT端口
        :param keepalive: 保持连接的心跳间隔时间（秒）
        :param reconnect_delay_set: 重连延迟设置，格式为(min_delay, max_delay)
        """
        self.broker_address = broker_address
        self.port = port
        self.keepalive = keepalive
        self.reconnect_delay_set = reconnect_delay_set
        self.client = mqtt.Client()

        # 设置自动重连的参数
        self.client.reconnect_delay_set(min_delay=reconnect_delay_set[0], max_delay=reconnect_delay_set[1])

    def on_connect(self, client, userdata, flags, rc):
        """
        当连接到MQTT服务器时的回调函数。
        """
        if rc == 0:
            logger.info("MQTT连接成功")
        else:
            logger.error("MQTT连接失败，返回码：", rc)

    def on_disconnect(self, client, userdata, rc):
        """
        当与MQTT服务器断开连接时的回调函数。
        """
        logger.info("断开MQTT连接，返回码：", rc)
        # 重新连接
        self.client.reconnect_delay_set(min_delay=self.reconnect_delay_set[0], max_delay=self.reconnect_delay_set[1])
        self.client.loop_start()  # 重新启动网络循环

    def on_message(self, client, userdata, msg):
        """
        当接收到MQTT消息时的回调函数。
        """
        logger.info(f"收到消息： topic='{msg.topic}', message='{msg.payload.decode()}', QoS {msg.qos}")
        return msg

    def connect(self):
        """
        连接到MQTT服务器。
        """
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, self.port, self.keepalive)
        self.client.loop_start()  # 启动网络循环
        time.sleep(1)

    def subscribe(self, topic):
        """
        订阅MQTT主题。
        :param topic: MQTT主题
        """
        self.client.subscribe(topic)

    def publish(self, topic, message, qos=1):
        """
        发送MQTT消息。
        :param topic: MQTT主题
        :param message: 要发送的消息（可以是字符串或字典）
        """
        global json_message
        if isinstance(message, dict):
            # 确保消息内容使用UTF-8编码
            json_message = json.dumps(message, ensure_ascii=False).encode('utf-8')
        else:
            json_message = message
        self.client.publish(topic, json_message, qos)

    def is_connected(self):
        """
        检查客户端是否已连接。
        """
        if not self.client.is_connected():
            self.client.reconnect()
        return self.client.is_connected()

    def disconnect(self):
        """
        断开与MQTT服务器的连接。
        """
        self.client.loop_stop()  # 停止网络循环
        self.client.disconnect()


# 使用示例
if __name__ == "__main__":
    # MQTT服务器地址和端口
    broker_address = "127.0.0.1"
    port = 1883

    result_topic = "result/image"
    logs_topic = "/logs"
    suct_topic = "/suct/status"
    arm_topic = "/arm/status"

    # 创建MQTT客户端实例
    print("创建MQTT客户端实例")
    mqtt_client = MQTTClient(broker_address, port)

    # 连接到MQTT服务器
    print("连接到MQTT服务器")
    mqtt_client.connect()

    mesg = {
        "PCD_Statu": 1
    }
    print("发送消息")
    mqtt_client.publish("test/topic", mesg)
    time.sleep(1)  # 每1秒发送一次消息