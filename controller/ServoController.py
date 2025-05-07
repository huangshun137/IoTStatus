from util.HttpUtil import HttpTool


class Servo:
    def __init__(self, base_url, robot_id):
        """
        初始化控制器
        :param base_url: 机器人调度url
        :param robot_id: 机器人 ID
        """
        self.base_url = base_url
        self.robot_id = robot_id
        self.httpUtil = HttpTool(base_url)

    def check_servo_state(self):
        url = "/servo/control"
        date = {
            "servo_id": 1,
            "target_angle": 600
        }
        return self.httpUtil.post(url=url, payload=date)