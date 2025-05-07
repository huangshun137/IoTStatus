from model.CommonModel import *

class ArmStatus(EnumWithDesc):
    free = (1, "安全位置")
    action = (2, "运动中")
    error = (3, "异常")


# 使用示例
if __name__ == "__main__":
    # 获取数值和描述
    print(f"ControlMode: {ArmStatus.free.value} - {ArmStatus.free.desc}")
    print(f"{get_desc_by_value(ArmStatus, 1)}")
