import time

import requests
import json


class HttpTool:
    def __init__(self, base_url=None, timeout=5):
        """
        初始化工具类
        :param base_url: API 基础 URL
        :param timeout: 请求超时时间（秒）
        """
        self.base_url = base_url
        self.timeout = timeout

    def get(self, url=None, params=None, headers=None):
        """
        发送 GET 请求
        :param url: API 接口路径
        :param params: 请求参数（可选）
        :param headers: 请求头（可选）
        :return: 响应数据
        """
        full_url = url if not self.base_url else f"{self.base_url}{url}"
        headers = headers or {}

        try:
            response = requests.get(
                full_url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GET 请求失败: {e}")
            return None

    def post(self, url=None, payload=None, headers=None):
        """
        发送 POST 请求
        :param url: API 接口路径
        :param payload: 请求体（可选）
        :param headers: 请求头（可选）
        :return: 响应数据
        """
        full_url = url if not self.base_url else f"{self.base_url}{url}"
        headers = headers or {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                full_url,
                data=json.dumps(payload) if payload else None,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"POST 请求失败: {e}")
            return None


# 设置最大重试次数和延时时间（秒）
MAX_RETRIES = 5
DELAY = 2


def retry_request(func, *args, **kwargs):
    for attempt in range(MAX_RETRIES):
        res = func(*args, **kwargs)
        if res["code"] == 200:
            return res["data"]
        else:
            print(f"{func.__name__} 失败，正在尝试第{attempt + 1}次...")
            time.sleep(DELAY)
    print(f"{func.__name__} 失败，已达到最大尝试次数")
    return None
