import time
from util.HttpUtil import HttpTool


class Controller:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.baseUrl = "http://" + self.ip + ":" + str(self.port)
        self.httpTool = HttpTool(self.baseUrl)
        self.initHttp()
        
    def _retry_request(self, method, url, params=None, payload=None, json=None, headers=None, max_retries=3):
        """通用重试逻辑"""
        for attempt in range(max_retries + 1):
            _params = {}
            if params:
                _params["params"] = params
            if payload:
                _params["payload"] = payload
            if json:
                _params["json"] = json
            if headers:
                _params["headers"] = headers
            response = method(url, **_params)
            if response and response.get('code') == 0:
                return response
            elif attempt < max_retries:
                time.sleep(1)  # 等待1秒后重试
                print(f"Attempt {attempt + 1}/{max_retries}")
            else:
                print(f"Attempt {attempt + 1}/{max_retries}: HTTP Error {response['msg']}")
                raise Exception(f"Failed after {max_retries} attempts")

    def initHttp(self):
        """初始化HTTP请求 获取token"""
        url = "/arm/getArmSoftwareInfo"
        headers = {"Content-Type": "application/json"}
        response = self._retry_request(self.httpTool.post, url, headers=headers)
        self.token = response.get("data", {}).get("token_v")
        print("arm init success, token:", self.token)

    def check_arm_state(self):
        """查询机械臂末端当前关节位姿"""
        # url = "/arm/getCurrentArmState"
        """
        请求/arm/getCurrentArmState时，个别机械臂会报错，错误码为9，应该是返回数据不完整
        请求/arm/getArmAllState时，也是报错误码9的异常
        验证发现只能请求/arm/getJointDegree单独获取机械臂的关节角度，不能获取整个机械臂的状态
        """
        url = "/arm/getJointDegree"
        headers = {
            "Content-Type": "application/json",
            "token": self.token
        }
        response_data = self._retry_request(self.httpTool.get, url, headers=headers)
        if not response_data or response_data.get("code") != 0:
            return False
        data = response_data["data"]
        # if data["arm_state"]:
        #     data["arm_state"]["joint"] = [x / 1000 for x in data["arm_state"]["joint"]]
        #     data["arm_state"]["pose"] = [x / 1000 for x in data["arm_state"]["pose"]]
        # return data["arm_state"]
        return data
      
    def check_lift_state(self):
        """查询机械臂升降机构状态"""
        url = "/joint/getLiftState"
        headers = {
            "Content-Type": "application/json",
            "token": self.token
        }
        response_data = self._retry_request(self.httpTool.post, url, headers=headers)
        if not response_data or response_data.get("code") != 0:
            return False
        data = response_data["data"]
        return data
    
    def set_lift_pose(self, params):
        """设置机械臂升降机构高度"""
        url = "/joint/setLiftHeight"
        speed = params.get("speed", 40)
        height = params.get("height")
        headers = {
            "Content-Type": "application/json",
            "token": self.token
        }
        payload = {
            "speed": speed,
            "height": height
        }
        response_data = self._retry_request(self.httpTool.post, url, payload=payload, headers=headers)
        if not response_data or response_data.get("code") != 0:
            return {
                "ok": False,
                "msg": response_data.get("msg", "设置失败")
            }
        else:
            return {
                "ok": True,
                "msg": "设置成功"
            }
      
    