from model.CommonModel import *


class RobotControlMode(EnumWithDesc):
    """机器人控制模式枚举"""
    kControlModeUndefined = (0, "未定义的")
    kAuto = (1, "自动")
    kManual = (2, "手动")
    kMaintain = (3, "维护")


class RobotState(EnumWithDesc):
    """机器人自动模式状态枚举"""
    kStateUndefined = (0, "未定义的")
    kUninit = (1, "未初始化")
    kfree = (2, "空闲")
    kParking = (3, "泊车中")
    kTask = (4, "任务中")
    kWarning = (5, "警告")
    kFault = (6, "异常")
    kFollowing = (7, "跟随中")
    kCharging = (8, "充电中")
    kMapping = (9, "构图中")


class RobotType(EnumWithDesc):
    """机器人类型枚举"""
    kTypeUndefined = (0, "未定义的")
    kBaseRobot_200 = (1, "通用底盘")
    kPalletLiftRobot_500 = (11, "栈板平台举升")
    kShelfLiftRobot_500 = (21, "移动料车举升")
    kTractorRobot_500 = (31, "牵引机器人")
    kRollerRobot_500 = (41, "辊筒机器人")
    kComplexRobot = (50, "复合机器人统称")
    kArmRobot_14 = (61, "复合机械臂")


class TaskState(EnumWithDesc):
    """任务状态枚举"""
    kStateUndefined = (0, "未定义的")
    kInit = (1, "初始化")
    kReady = (2, "准备的")
    kExecuting = (3, "执行中")
    kPaused = (4, "暂停的")
    kActionWait = (5, "动作等待")
    kTaskWait = (6, "任务等待")
    kCompleted = (7, "完成的")
    kCanceled = (8, "取消的")
    kFailed = (9, "失败的")


class TaskType(EnumWithDesc):
    """任务类型枚举"""
    kTypeUndefined = (0, "未定义的")
    kPick = (1, "拣选")
    kParking = (2, "泊车")
    kCharge = (3, "充电")
    kCarry = (4, "搬运")


class Error(EnumWithDesc):
    """机械臂控制器返回状态码枚举"""
    SUCCESS = (0, "成功")
    PARAM_ERROR = (1, "控制器返回 false，参数错误或机械臂状态异常")
    SEND_FAILED = (-1, "数据发送失败，通信异常")
    RECV_FAILED = (-2, "数据接收失败或超时")
    PARSE_FAILED = (-3, "返回值解析失败，数据格式不正确或不完整")
    DEVICE_MISMATCH = (-4, "当前到位设备校验失败")
    TIMEOUT = (-5, "单线程阻塞模式,超时未接收到返回")

from pydantic import BaseModel, Field
from typing import Optional

class WooshState(BaseModel):
    """
    机器人选择数据传输对象
    """
    robot_id: Optional[int] = Field(None, description="底盘id", alias="robotId")
    state: Optional[str] = Field(None, description="状态", alias="state")
    state_desc: Optional[str] = Field(None, description="状态name", alias="state_desc")
    class Config:
        allow_population_by_field_name = True  # 允许通过别名填充字段


# 示例
if __name__ == "__main__":
    # 获取数值和描述
    print(f"ControlMode: {RobotControlMode.kAuto.value} - {RobotControlMode.kAuto.desc}")
    print(f"{get_desc_by_value(TaskType, 1)}")
