import math
import time
from common import config
import urllib.parse

from util.HttpUtil import *

class Water:
    def __init__(self, ip_address):
        self.base_url = ip_address
        self.httpTool = HttpTool(self.base_url)

    def _retry_request(self, method, url, params=None, max_retries=3):
        """通用重试逻辑"""
        for attempt in range(max_retries + 1):
            response = method(url, params=params)
            if response.get('status') == 'OK':
                return response
            else:
                print(f"Attempt {attempt + 1}/{max_retries}")
        else:
            print(f"Attempt {attempt + 1}/{max_retries}: HTTP Error {response.status_code}")
        if attempt < max_retries:
            time.sleep(1)  # 等待1秒后重试
        raise Exception(f"Failed after {max_retries} attempts")

    def get_robot_info(self):
        """获取机器人信息(只能获取机器人编号)"""
        url = f"/api/robot_info"
        response_data = self._retry_request(self.httpTool.get, url)
        return response_data["results"]

    def get_robot_status(self):
        """获取机器人当前全局状态"""
        url = f"/api/robot_status"
        response_data = self._retry_request(self.httpTool.get, url)
        return response_data["results"]

    def get_robot_battery_info(self):
        """获取底盘电池信息"""
        url = f"/api/get_power_status"
        response_data = self._retry_request(self.httpTool.get, url)
        return response_data["results"]

    def move_to_marker(self, marker_name):
        """导航到指定的点位"""
        url = f"/api/move"
        params = {
            "marker": marker_name
        }
        response_data = self._retry_request(self.httpTool.get, url, params=params)
        return response_data.get('task_id', 'Task ID not provided')

    def move_to_pose(self, x, y, theta):
        """导航到指定坐标朝向"""
        url = f"/api/move?location={x},{y},{theta}"
        response_data = self._retry_request(self.httpTool.get, url)
        return response_data

    def cancel_move(self):
        """取消当前导航"""
        url = f"/api/move/cancel"
        response_data = self._retry_request(self.httpTool.get, url)
        return response_data

    def request_water_api(self, url, params={}, method="get"):
        """
        请求 Woosh 底盘api
        :param url: 请求 URL
        :param params: 请求参数
        :return: 响应数据
        """
        if (method == "get"):
            # 构建查询字符串
            del params['optionValue']
            del params['requestUrl']
            query_string = urllib.parse.urlencode(params).replace("True", "true").replace("False", "false")
            print(query_string)
            response = self.httpTool.get(f"{url}?{query_string}")
            return response


# 使用示例
if __name__ == "__main__":
    water = Water(config.water_ip)

    try:
        # 获取机器人状态
        status = water.get_cur_map()
        print("Robot Status:", status)

        # # 导航到指定点位
        # task_id = water.move_to_marker("B1")
        # print(f"Navigation task started with task ID: {task_id}")

    except Exception as e:
        print(str(e))