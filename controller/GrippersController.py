from Robotic_Arm.rm_robot_interface import *

import common.config
from model.CommonModel import get_desc_by_value
from model.GripperModel import GripperStatus
from util.log_util import default_logger as logger


class GripperControlWrapper:
    """
    机械臂实例 (RoboticArm) 已由外部提供。
    """

    def __init__(self, arm: RoboticArm):
        """
        初始化夹爪控制工具类
        :param arm: 已实例化的机械臂对象 (RoboticArm)
        :param debug: 是否启用调试模式，启用时会打印详细日志
        """
        self._arm = arm

    def set_gripper_route(self, min_route: int, max_route: int) -> bool:
        """
        设置夹爪开口的最大值和最小值
        :param min_route: 夹爪开口最小值 (0 ~ 1000)
        :param max_route: 夹爪开口最大值 (0 ~ 1000)
        :return: 操作是否成功
        """
        if not (0 <= min_route <= 1000 and 0 <= max_route <= 1000):
            logger.warning("夹爪开口范围超出有效范围 (0~1000)")
            return False

        result = self._arm.rm_set_gripper_route(min_route, max_route)
        if result == 0:
            logger.info(f"夹爪开口范围设置成功: min={min_route}, max={max_route}")
            return True
        else:
            logger.error(f"设置夹爪开口范围失败。错误代码: {result}")
            return False

    def release_gripper(self, speed: int, block: bool = True, timeout: int = 10) -> bool:
        """
        松开夹爪到开口最大处
        :param speed: 夹爪松开速度 (1 ~ 1000)
        :param block: 是否阻塞模式
        :param timeout: 阻塞模式下的超时时间 (单位: 秒)
        :return: 操作是否成功
        """
        if not (1 <= speed <= 1000):
            logger.warning("松开速度超出有效范围 (1~1000)")
            return False

        result = self._arm.rm_set_gripper_release(speed, block, timeout)
        if result == 0:
            logger.info(f"夹爪松开成功。速度: {speed}")
            return True
        else:
            logger.error(f"夹爪松开失败。错误代码: {result}")
            return False

    def pick_up(self, speed: int, force: int, block: bool = True, timeout: int = 10) -> bool:
        """
        夹爪力控夹取
        :param speed: 夹爪夹取速度 (1 ~ 1000)
        :param force: 力控阈值 (50 ~ 1000)
        :param block: 是否阻塞模式
        :param timeout: 阻塞模式下的超时时间 (单位: 秒)
        :return: 操作是否成功
        """
        if not (1 <= speed <= 1000) or not (50 <= force <= 1000):
            logger.warning("速度或力值超出有效范围 (速度:1~1000, 力值:50~1000)")
            return False

        result = self._arm.rm_set_gripper_pick(speed, force, block, timeout)
        if result == 0:
            logger.info(f"夹爪力控夹取成功。速度: {speed}, 力值: {force}")
            return True
        else:
            logger.error(f"夹爪力控夹取失败。错误代码: {result}")
            return False

    def hold_pick_up(self, speed: int, force: int, block: bool = True, timeout: int = 10) -> bool:
        """
        夹爪持续力控夹取
        :param speed: 夹爪夹取速度 (1 ~ 1000)
        :param force: 力控阈值 (50 ~ 1000)
        :param block: 是否阻塞模式
        :param timeout: 阻塞模式下的超时时间 (单位: 秒)
        :return: 操作是否成功
        """
        if not (1 <= speed <= 1000) or not (50 <= force <= 1000):
            logger.warning("速度或力值超出有效范围 (速度:1~1000, 力值:50~1000)")
            return False

        result = self._arm.rm_set_gripper_pick_on(speed, force, block, timeout)
        if result == 0:
            logger.info(f"夹爪持续力控夹取成功。速度: {speed}, 力值: {force}")
            return True
        else:
            logger.error(f"夹爪持续力控夹取失败。错误代码: {result}")
            return False

    def set_gripper_position(self, position: int, block: bool = True, timeout: int = 10) -> bool:
        """
        设置夹爪开口到指定位置
        :param position: 夹爪开口位置 (1 ~ 1000)
        :param block: 是否阻塞模式
        :param timeout: 阻塞模式下的超时时间 (单位: 秒)
        :return: 操作是否成功
        """
        if not (1 <= position <= 1000):
            logger.warning("指定位置超出有效范围 (1~1000)")
            return False

        result = self._arm.rm_set_gripper_position(position, block, timeout)
        if result == 0:
            logger.info(f"夹爪开口位置设置成功: {position}")
            return True
        else:
            logger.error(f"设置夹爪开口位置失败。错误代码: {result}")
            return False

    def get_gripper_state(self) -> dict:
        """
        获取夹爪状态
        :return: 夹爪状态信息 -
        {'enable_state': 0, 'status': 0, 'error': 0, 'mode': 0, 'current_force': 0, 'temperature': 0, 'actpos': 0}
        - enable_state (int): 夹爪使能标志，0 表示未使能，1 表示使能
        - status (int): 夹爪在线状态，0 表示离线， 1表示在线
        - error (int): 夹爪错误信息，低8位表示夹爪内部的错误信息bit5-7 保留bit4 内部通bit3 驱动器bit2 过流 bit1 过温bit0 堵转
        - mode (int): 当前工作状态：1 夹爪张开到最大且空闲，2 夹爪闭合到最小且空闲，3 夹爪停止且空闲，4 夹爪正在闭合，5 夹爪正在张开，6 夹爪闭合过程中遇到力控停止
        - current_force (int): 夹爪当前的压力，单位g
        - temperature (int): 当前温度，单位℃
        - actpos (int): 夹爪开口度
        """
        result, state = self._arm.rm_get_gripper_state()
        if result == 0:
            logger.info(f"成功获取夹爪状态{state}")
            state["enable_state_desc"] = get_desc_by_value(GripperStatus, state["enable_state"])
            state["status_desc"] = get_desc_by_value(GripperStatus, state["status"])
            state["mode_desc"] = get_desc_by_value(GripperStatus, state["mode"])
            return state
        else:
            logger.error(f"获取夹爪状态失败。错误代码: {result}")
            return {}
        
    def set_gripper_status(self, flag, write_params) -> bool:
        """
        设置夹爪状态
        :param flag: 使能标志，0 表示未使能，1 表示使能
        :return: 操作是否成功
        """
        data = [0, 9, 255, 0, 255, 255] if flag == "close" else [0, 9, 0, 0, 255, 255]
        result = self._arm.rm_write_registers(self, write_params, data)
        if result == 0:
            logger.info(f"夹爪状态设置成功: {flag}")
            return True
        else:
            logger.error(f"设置夹爪状态失败。错误代码: {result}")
            return False



# 使用示例
if __name__ == "__main__":
    from Robotic_Arm.rm_robot_interface import *

    # 实例化RoboticArm类
    arm_left = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)

    # 创建机械臂连接，打印连接id
    handle = arm_left.rm_create_robot_arm("169.254.128.18", 8080)

    print(arm_left.rm_set_gripper_pick(500, 1000, True, 10))

    arm_left.rm_delete_robot_arm()

    # 初始化夹爪工具类，启用调试模式
    #gripper = GripperControlWrapper(arm)

    # 示例操作
    # 设置夹爪开口范围
    # if gripper.set_gripper_route(80, 280):
    #     print("夹爪开口范围设置成功")
    # else:
    #     print("夹爪开口范围设置失败")

    # 松开夹爪
    # if gripper.release_gripper(100, block=True, timeout=5):
    #     print("夹爪已松开")
    # else:
    #     print("夹爪松开失败")
    #
    # 力控夹取 力控达到的目标值就停止
    # if gripper.pick_up(500, 1000, block=True, timeout=5):
    #     print("夹爪已夹取物体")
    # else:
    #     print("夹爪夹取失败")

    # # 持续力控夹取，一直发力直到让夹爪停止
    # if gripper.hold_pick_up(50, 200, block=True, timeout=5):
    #     print("夹爪已持续力控夹取")
    # else:
    #     print("夹爪持续力控夹取失败")
    #
    # # 设置夹爪位置
    # if gripper.set_gripper_position(500, block=True, timeout=5):
    #     print("夹爪位置设置成功")
    # else:
    #     print("夹爪位置设置失败")

    # 获取夹爪状态
    #state = gripper.get_gripper_state()
