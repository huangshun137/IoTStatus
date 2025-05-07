import json

import common.config as config
from model.WooshModel import *
from util.HttpUtil import HttpTool


class Woosh:
    def __init__(self, base_url, robot_id):
        """
        初始化控制器
        :param base_url: 机器人调度url
        :param robot_id: 机器人 ID
        """
        self.base_url = base_url
        self.robot_id = robot_id
        self.httpUtil = HttpTool(base_url)

    def  get_cur_pose(self, woosh_id):
        """
        当前状态位置姿态
        """
        payload = {
          "robotId": woosh_id
        }
        return self.httpUtil.post("/woosh/robot/PoseSpeed", payload)

    def  get_cur_state(self, woosh_id):
        """
        当前状态位置姿态
        """
        payload = {
          "robotId": woosh_id
        }
        return self.httpUtil.post("/woosh/robot/RobotState", payload)

    def check_initialization(self):
        """
        检查机器人是否初始化
        :return: 初始化状态
        """
        payload = {"isRecord": False}
        print("切换地图")
        return self.httpUtil.post("/woosh/robot/InitRobot", payload)

    def check_status_codes(self):
        """
        检查机器人状态码
        :return: 状态码信息
        """
        payload = {}
        return self.httpUtil.post("/woosh/robot/count/StatusCodes", payload)

    def check_abnormal_codes(self):
        """
        检查机器人异常码
        :return: 异常码信息
        """
        payload = {}
        return self.httpUtil.post("/woosh/robot/count/AbnormalCodes", payload)

    def check_task_state(self):
        """
        检查任务进度
        :param task_id: 任务 ID
        :return: 任务进度信息
        """
        payload = {"robotId": self.robot_id}
        response = self.httpUtil.post("/woosh/robot/TaskProc", payload)
        print(f"检查任务状态{response}")
        if response:
            status = response
            action_status = status.get('body', {}).get('state', -1)
            print(f"当前任务状态-{get_desc_by_value(TaskState, action_status)}")
            if action_status in (TaskState.kCompleted.value, TaskState.kStateUndefined.value):
                print("任务已完成")
                return True
            if action_status in (TaskState.kCanceled.value, TaskState.kFailed.value):
                print("任务失败")
                return False
        else:
            print(f"查询状态失败，状态码: {response.status_code}")
            return None
        
    def get_robot_info(self):
        """
        获取机器人信息
        :param robotId: 机器人 ID
        :return: 机器人信息
        """
        payload = {"robotId": self.robot_id}
        response = self.httpUtil.post("/woosh/robot/RobotInfo", payload)
        if response:
            status = response
            woosh_info = status.get('body', {})
            return woosh_info
        else:
            print(f"查询状态失败，状态码: {response.status_code}")
            return None

    def check_robot_state(self):
        """
        检查任务进度
        :param task_id: 任务 ID
        :return: 任务进度信息

        {'body': {'robotId': 10001, 'state': 2}, 'msg': 'Request succeed', 'ok': True, 'type': 'woosh.robot.RobotState'}
        """
        payload = {"robotId": self.robot_id}
        response = self.httpUtil.post("/woosh/robot/RobotState", payload)
        print(f"检查机器人状态{response}")
        if response:
            status = response
            woosh_statu = status.get('body', {})
            action_status = status.get('body', {}).get('state', -1)
            woosh_statu['state_desc'] = get_desc_by_value(RobotState, action_status)
            print(f"当前机器人状态-{woosh_statu['state_desc']}")
            return woosh_statu
        else:
            print(f"查询状态失败，状态码: {response.status_code}")
            return None

    def print_response(self, response):
        """
        打印响应结果
        :param response: 响应数据
        """
        if response:
            print("请求成功，响应数据：")
            print(json.dumps(response, indent=4))
        else:
            print("请求失败，请检查错误信息。")

    def request_woosh_api(self, url, params = {}, method = "post"):
        """
        请求 Woosh 底盘api
        :param url: 请求 URL
        :param params: 请求参数
        :return: 响应数据
        """
        if (method == "post"):
            params["robotId"] = self.robot_id
            response = self.httpUtil.post(url, params)
            return response


# 使用示例
if __name__ == "__main__":
    # 配置机器人信息
    robot_base_url = config.woosh_ip
    robot_id = config.woosh_id  # 替换为实际的机器人 ID
    target_points = ["H3"]  # 多个目标点编号

    # 初始化控制器
    controller = WooshRobotController(base_url=robot_base_url, robot_id=robot_id)

    # 检查机器人是否初始化
    print("检查机器人是否初始化：")
    init_status = controller.check_initialization()
    controller.print_response(init_status)
    if not init_status or not init_status.get("ok"):
        print("初始化检查失败，无法继续操作。")
        exit()

    # 检查机器人状态码
    print("检查机器人状态码：")
    status_codes = controller.check_status_codes()
    controller.print_response(status_codes)
    if not status_codes or not status_codes.get("ok"):
        print("状态码检查失败，无法继续操作。")
        exit()

    # 检查机器人异常码
    print("检查机器人异常码：")
    abnormal_codes = controller.check_abnormal_codes()
    controller.print_response(abnormal_codes)
    if not abnormal_codes or not abnormal_codes.get("ok"):
        print("异常码检查失败，无法继续操作。")
        exit()

    # 导航到多个目标点
    print("导航到多个目标点：")
    controller.navigate_to_points(target_points)
