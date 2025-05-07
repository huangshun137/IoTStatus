import threading
import time

from Robotic_Arm.rm_robot_interface import *
import common.config as config
from controller import GrippersController, UploadStatus
from model.ArmModel import *
from model.GripperModel import *
from model.LiftModel import *
from util.log_util import default_logger as logger

# 实例创建锁
arm_lock = threading.Lock()
# 升降机构状态控制
arm_lock2 = threading.Lock()  # 状态访问的锁
is_life = False  # 共享状态


class ArmController:
    def __init__(self, ip_address, port, is_double=None):
        if is_double == 3:
            self.arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
        else:
            self.arm = RoboticArm()
        self.handle = None
        self.ip_address = ip_address
        self.port = port
        
        self.gripper = GrippersController.GripperControlWrapper(self.arm)

    def create_robot_arm(self):
        with arm_lock:
            self.handle = self.arm.rm_create_robot_arm(self.ip_address, self.port)
            if self.handle is None:
                print(f"创建机械臂连接失败。")
                return False
            print(f"机械臂连接已创建。")
            return True

    def get_cur_pose(self):
        result, degree = self.arm.rm_get_joint_degree()
        if result == 0:
            # print(f"机器人当前关节角度：{degree}")
            return degree
        else:
            return None

    def check_arm_state(self):
        result, arm_state = self.arm.rm_get_current_arm_state()
        if result == 0:
            # print(f"机器人当前状态：{arm_state}")

            return arm_state
        else:
            return None

    def check_gripper_state(self) -> dict:
        """获取夹爪状态"""
        return self.gripper.get_gripper_state()

    def check_lift_state(self) -> dict:
        """
        升降机构状态
        - pos (int): 扩展关节角度，单位度，精度 0.001°(若为升降机构高度，则s单位：mm，精度：1mm，范围：0 ~2300)
        - current (int): 驱动电流，单位：mA，精度：1mA
        - err_flag (int): 驱动错误代码，错误代码类型参考关节错误代码
        - mode (int): 当前工作状态
            - 0：空闲
            - 1：正方向速度运动
            - 2：正方向位置运动
            - 3：负方向速度运动
            - 4：负方向位置运动
        """
        result, state = self.arm.rm_get_lift_state()
        if result == 0:
            # print(f"升降机构状态： {state}")
            state["mode_desc"] = get_desc_by_value(LiftStatus, state["mode"])
            return state
        else:
            return {}

    def set_gripper_status(self, params) -> bool:
        """
        设置夹爪状态
        :param flag: close: 全关；open: 全开
        :return: 操作是否成功
        """
        # write_params = {
        #     "port": 1,
        #     "address": 1000,
        #     "device": 9,
        #     "num": 3
        # }
        flag = params.get("flag")
        write_params = rm_peripheral_read_write_params_t(1, 1000, 9, 3)
        print(f"设置夹爪状态: {flag}， {write_params}")
        data = [0, 9, 255, 0, 255, 255] if flag == "close" else [0, 9, 0, 0, 255, 255]
        result = self.arm.rm_write_registers(write_params, data)
        if result == 0 or result == 1:
            logger.info(f"夹爪状态设置成功: {flag}")
            return {
                "ok": True,
                "msg": "请求成功"
            }
        else:
            logger.error(f"设置夹爪状态失败。错误代码: {result}")
            return {
                "ok": False,
                "msg": "请求失败"
            }
        # return self.gripper.set_gripper_status(flag, write_params)

    def set_lift_pose(self, params):
        """
        设置升降机构高度
        :param height: 升降机构高度，单位mm，范围：0 ~ 2300
        :return: 操作是否成功
        """
        speed = params.get("speed", 40)
        height = params.get("height")
        block = params.get("block", 1)
        if not height:
            logger.warning("升降机构高度未设置")
            return {
                "ok": False,
                "msg": "升降机构高度未设置"
            }
        result = self.arm.rm_set_lift_height(speed, height, block)
        if result == 0:
            logger.info(f"升降机构高度设置成功: {height}")
            return {
                "ok": True,
                "msg": "设置成功"
            }
        else:
            logger.error(f"设置升降机构高度失败。错误代码: {result}")
            return {
                "ok": False,
                "msg": "设置失败"
            }

    def switch_to_base_frame(self):
        return self.arm.rm_change_work_frame("Base") == 0

    def delete(self):
        self.arm.rm_delete_robot_arm()
        print(f"机械臂连接已关闭")


# 升降台控制
def lift_run(left_arm_controller, target_lift_height, publisher):
    global is_life
    if target_lift_height:
        left_arm_controller.triger_lift(target_lift_height)
        publisher.updateStates(lift_state=LiftStatus.kUpSpeed.value)
        while True:
            lift_state = left_arm_controller.check_lift_state()
            print(f"升降台状态{lift_state}")
            if lift_state["mode"] == LiftStatus.kfree.value:
                publisher.updateStates(lift_state=LiftStatus.kfree.value)
                break
        with arm_lock2:  # 安全修改
            is_life = True
            print(f"左臂设置状态: {is_life}")
    else:
        with arm_lock2:
            is_life = True
            print("左臂强制激活状态")


def right_run(target_pose, gripper_on, publisher: UploadStatus.MqttPublisher, right_arm_controller):
    global is_life
    while True:
        time.sleep(0.06)
        if is_life:
            # 执行主逻辑
            publisher.updateStates(arm_state=ArmStatus.action.value)
            if right_arm_controller.movej_to_target(target_pose):
                if gripper_on:
                    publisher.updateStates(gripper_state=GripperStatus.kClosing.value)
                    right_arm_controller.gripper_pickon()
                    while True:
                        time.sleep(1)
                        state = right_arm_controller.check_gripper_state()
                        if state["mode"] in (GripperStatus.kForceStopped.value,):
                            publisher.updateStates(gripper_state=GripperStatus.kForceStopped.value)
                            break
                else:
                    publisher.updateStates(gripper_state=GripperStatus.kOpening.value)
                    right_arm_controller.gripper_release()
                    while True:
                        time.sleep(1)
                        state = right_arm_controller.check_gripper_state()
                        if state["mode"] in (GripperStatus.kIdleOpen.value,):
                            publisher.updateStates(gripper_state=GripperStatus.kForceStopped.value)
                            break

            right_arm_controller.movej_to_init_pose(config.right_init_pose)
            publisher.updateStates(arm_state=ArmStatus.free.value)
            break


def left_run(target_pose, gripper_on, publisher: UploadStatus.MqttPublisher, left_arm_controller):
    global is_life
    while True:
        time.sleep(0.05)
        if is_life:
            # 手臂运动到指定位置
            publisher.updateStates(arm_state=ArmStatus.action.value)
            if left_arm_controller.movej_to_target(target_pose):
                # 控制夹爪
                if gripper_on:
                    publisher.updateStates(gripper_state=GripperStatus.kClosing.value)
                    left_arm_controller.gripper_pickon()
                    while True:
                        time.sleep(1)
                        state = left_arm_controller.check_gripper_state()
                        if state["mode"] in (GripperStatus.kForceStopped.value,):
                            publisher.updateStates(gripper_state=GripperStatus.kForceStopped.value)
                            break
                else:
                    publisher.updateStates(gripper_state=GripperStatus.kOpening.value)
                    left_arm_controller.gripper_release()
                    while True:
                        time.sleep(1)
                        state = left_arm_controller.check_gripper_state()
                        if state["mode"] in (GripperStatus.kIdleOpen.value,):
                            publisher.updateStates(gripper_state=GripperStatus.kForceStopped.value)
                            break

            left_arm_controller.movej_to_init_pose(config.left_init_pose)
            publisher.updateStates(arm_state=ArmStatus.free.value)
            break
