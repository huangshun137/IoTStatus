from model.CommonModel import *

class GripperStatus(EnumWithDesc):
    """夹爪状态枚举"""
    kIdleOpen = (1, "夹爪张开到最大且空闲")
    kIdleClosed = (2, "夹爪闭合到最小且空闲")
    kIdleStopped = (3, "夹爪停止且空闲")
    kClosing = (4, "夹爪正在闭合")
    kOpening = (5, "夹爪正在张开")
    kForceStopped = (6, "夹爪闭合过程中遇到力控停止")


# 使用示例
if __name__ == "__main__":
    # 获取数值和描述
    print(f"ControlMode: {GripperStatus.kIdleOpen.value} - {GripperStatus.kIdleOpen.desc}")
    print(f"{get_desc_by_value(GripperStatus, 1)}")
