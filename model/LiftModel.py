from model.CommonModel import *


class LiftStatus(EnumWithDesc):
    """升降机构状态枚举"""
    kfree = (0, "空闲")
    kUpSpeed = (1, "正方向速度运动")
    kUpPosition = (2, "正方向位置运动")
    kDownSpeed = (3, "负方向速度运动")
    kDownPosition = (4, "负方向位置运动")


# 使用示例
if __name__ == "__main__":
    # 获取数值和描述
    print(f"ControlMode: {LiftStatus.kUpPosition.value} - {LiftStatus.kUpPosition.desc}")
    print(f"{get_desc_by_value(LiftStatus, 1)}")
