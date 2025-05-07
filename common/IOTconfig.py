from enum import Enum, auto


class TopicType(Enum):
    DEVICE_MESSAGE_UP = auto()
    """设备消息上报"""

    DEVICE_MESSAGE_DOWN = auto()
    """# 平台下发消息给设备"""

    DEVICE_COMMAND_REQUEST = auto()
    """# 平台下发命令给设备"""

    DEVICE_COMMAND_RESPONSE = auto()
    """# 设备返回命令响应"""

    DEVICE_PROPERTIES_REPORT = auto()
    """# 设备上报属性数据"""

    DEVICE_PROPERTIES_SET_REQUEST = auto()
    """# 平台设置设备属性"""

    DEVICE_PROPERTIES_SET_RESPONSE = auto()
    """# 属性设置的响应结果"""

    DEVICE_PROPERTIES_GET = auto()
    """# 平台查询设备属性"""

    DEVICE_EVENT_UP = auto()
    """# 设备事件上报"""


class DeviceTopic:
    def __init__(self, device_id):
        # 初始化时接收设备ID
        self.device_id = device_id

    def get_topic(self, topic_type):
        """
        根据给定的Topic类型生成Topic路径。

        :param topic_type: 枚举类型，表示需要哪种类型的Topic
        :return: 生成的Topic路径字符串
        """
        if topic_type == TopicType.DEVICE_MESSAGE_UP:
            # 设备消息上报的Topic路径
            return f"/devices/{self.device_id}/sys/messages/up"
        elif topic_type == TopicType.DEVICE_MESSAGE_DOWN:
            # 平台下发消息给设备的Topic路径
            return f"/devices/{self.device_id}/sys/messages/down"
        elif topic_type == TopicType.DEVICE_COMMAND_REQUEST:
            # 平台下发命令给设备的Topic路径，需要用户输入request_id
            # request_id = input("Enter request_id for command: ")
            return f"/devices/{self.device_id}/sys/commands/#"
        elif topic_type == TopicType.DEVICE_COMMAND_RESPONSE:
            # 设备返回命令响应的Topic路径，需要用户输入request_id
            # request_id = input("Enter request_id for command response: ")
            return f"/devices/{self.device_id}/sys/commands/response/request_id="
        elif topic_type == TopicType.DEVICE_PROPERTIES_REPORT:
            # 设备上报属性数据的Topic路径
            return f"/devices/{self.device_id}/sys/properties/report"
        elif topic_type == TopicType.DEVICE_PROPERTIES_SET_REQUEST:
            # 平台设置设备属性的Topic路径，需要用户输入request_id
            # request_id = input("Enter request_id for properties set: ")
            return f"/devices/{self.device_id}/sys/properties/set/#"
        elif topic_type == TopicType.DEVICE_PROPERTIES_SET_RESPONSE:
            # 属性设置的响应结果的Topic路径，需要用户输入request_id
            # request_id = input("Enter request_id for properties set response: ")
            return f"/devices/{self.device_id}/sys/properties/set/response/request_id="
        elif topic_type == TopicType.DEVICE_PROPERTIES_GET:
            # 平台查询设备属性的Topic路径
            return f"/devices/{self.device_id}/sys/properties/get"
        elif topic_type == TopicType.DEVICE_EVENT_UP:
            # 设备事件上报的Topic路径
            return f"/devices/{self.device_id}/sys/events/up"
        else:
            # 如果传入了未知的Topic类型，则抛出异常
            raise ValueError("Unknown topic type")


# 使用示例
topic = DeviceTopic("device_id")  # 创建DeviceTopic实例
topic_path = topic.get_topic(TopicType.DEVICE_MESSAGE_UP)
