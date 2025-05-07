from util.HttpUtil import HttpTool

class Camera:
    def __init__(self, base_url):
        """
        初始化控制器
        :param base_url: 机器人调度url
        :param robot_id: 机器人 ID
        """
        self.base_url = base_url
        self.httpUtil = HttpTool(base_url)

    def check_camera_state(self):
        return self.httpUtil.get(url="/snapshoot")