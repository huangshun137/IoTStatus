# todo 通过简单json指令控制机械臂
import json
import socket
import time


class Controller:
    def __init__(self, ip_address, port):
        self.robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.robot_socket.connect((ip_address, port))
        print("=============成功连接机械臂=============")

    def check_arm_state(self):
        """
        查询机械臂末端当前关节位姿
        :return:
        """
        try:
            json_str = json.dumps({"command": "get_current_arm_state"})
            self.robot_socket.sendall((json_str + "\n").encode("utf-8"))
            # print(f"已发送机械臂指令: {json_str}")
            response = self.robot_socket.recv(1024).decode("utf-8")
            # data = json.loads(response)
            if not response:
                print("===========服务器断开，请查看连接是否正常============")
                # 直接返回
                return False
            else:
                # print(f"响应内容为{response}")
                data = json.loads(response)
                data["arm_state"]["joint"] = [x / 1000 for x in data["arm_state"]["joint"]]
                data["arm_state"]["pose"] = [x / 1000 for x in data["arm_state"]["pose"]]
                return data["arm_state"]
        except Exception as e:
            print("=============机械臂指令发送失败===============")
            return False

    def check_lift_state(self):
        """
        查询机械臂末端当前关节位姿
        :return:
        """
        try:
            json_str = json.dumps({"command": "get_lift_state"})
            self.robot_socket.sendall((json_str + "\n").encode("utf-8"))
            # print(f"已发送机械臂指令: {json_str}")
            response = self.robot_socket.recv(1024).decode("utf-8")
            # data = json.loads(response)
            # pose = data["arm_state"]["pose"]
            if not response:
                print("===========服务器断开，请查看连接是否正常============")
                # 直接返回
                return False
            else:
                # print(f"响应内容为{response}")
                return json.loads(response)
        except Exception as e:
            print("=============机械臂指令发送失败===============")
            return False

    def set_lift_pose(self, params):
      speed = params.get("speed", 40)
      height = params.get("height")
      command = {"command": "set_lift_height", "height": height, "speed": speed}
      if not height:
          return {
              "ok": False,
              "msg": "升降机构高度未设置"
          }
      # 用于累积接收到的数据
      buffer = ""
      # 开始时间
      start_time = time.time()
      timeout = 3
      try:
          # 将json指令转换为字符串
          json_str = json.dumps(command)
          # 发送json指令
          self.robot_socket.sendall((json_str + "\n").encode("utf-8"))
          print(f"已发送机械臂指令: {json_str}")
          # 循环查看响应内容（{"command":"发送的指令是什么","receive_state":true}）
          while True:
              response = self.robot_socket.recv(1024).decode("utf-8")
              if not response:
                  # 直接返回
                  return {
                      "ok": False,
                      "msg": "设置失败"
                  }
              buffer += response
              while "\n" in buffer:
                  message, buffer = buffer.split("\n", 1)
                  try:
                      parsed_message = json.loads(message)
                      print(f"响应内容为{parsed_message}")
                      # 对响应内容进行提取关键信息
                      if parsed_message.get("trajectory_state", False) == True:
                          return {
                              "ok": True,
                              "msg": "设置成功"
                          }
                  except json.JSONDecodeError:
                      buffer = message + "\n" + buffer
                      break
              # 超时处理
              if time.time() - start_time > timeout:
                  print("============响应超时============")
                  return {
                      "ok": False,
                      "msg": "设置失败"
                  }
      except Exception as e:
          print("=============机械臂指令发送失败===============", e)
          return {
              "ok": False,
              "msg": "设置失败"
          }
