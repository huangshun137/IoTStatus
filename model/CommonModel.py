from enum import Enum

class EnumWithDesc(Enum):
    """带有描述信息的枚举基类"""
    def __new__(cls, value, desc):
        member = object.__new__(cls)
        member._value_ = value  # 状态码
        member.desc = desc  # 描述信息
        return member


def get_desc_by_value(enum_class, value):
    """根据数值获取枚举类的描述信息"""
    if isinstance(value, (int, float)):
        for member in enum_class:
            if member.value == value:
                return member.desc
        return "Not found"
    else:
        return value