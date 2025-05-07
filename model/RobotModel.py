from typing import Optional, List
from pydantic import BaseModel, Field

class MapInfo(BaseModel):
    """
    地图信息
    """
    map_id: Optional[int] = Field(None, description="地图ID", alias="mapId")
    map_code: Optional[str] = Field(None, description="地图编码", alias="mapCode")
    map_name: Optional[str] = Field(None, description="地图名称", alias="mapName")
    url: Optional[str] = Field(None, description="地图URL", alias="url")
    map_img: Optional[str] = Field(None, description="地图图片", alias="mapImg")
    map_type: Optional[str] = Field(None, description="地图类型", alias="mapType")
    is_action: Optional[str] = Field(None, description="是否启用", alias="isAction")
    regist_user_id: Optional[str] = Field(None, description="创建人", alias="registUserId")
    regist_date: Optional[str] = Field(None, description="创建时间", alias="registDate")
    update_user_id: Optional[str] = Field(None, description="更新人", alias="updateUserId")
    update_date: Optional[str] = Field(None, description="更新时间", alias="updateDate")

class SelectRobotDTO(BaseModel):
    """
    机器人选择数据传输对象
    """
    robot_id: Optional[int] = Field(None, description="机器人编号", alias="robotId")
    robot_name: Optional[str] = Field(None, description="机器人名称", alias="robotName")
    robot_num: Optional[str] = Field(None, description="机器人编号", alias="robotNum")
    robot_code: Optional[str] = Field(None, description="底盘代码", alias="robotCode")
    robot_ip: Optional[str] = Field(None, description="底盘IP", alias="robotIp")
    robot_mac: Optional[str] = Field(None, description="底盘MAC", alias="robotMac")
    robot_type: Optional[str] = Field(None, description="机器人类型", alias="robotType")
    is_action: Optional[str] = Field(None, description="是否开启 (1-开，0-关)", alias="isAction")
    robot_describe: Optional[str] = Field(None, description="机器人描述", alias="robotDescribe")
    regist_user_id: Optional[str] = Field(None, description="创建人", alias="registUserId")
    regist_date: Optional[str] = Field(None, description="创建时间", alias="registDate")
    update_user_id: Optional[str] = Field(None, description="更新人", alias="updateUserId")
    update_date: Optional[str] = Field(None, description="更新时间", alias="updateDate")
    map_id: Optional[int] = Field(None, description="机器人所属地图", alias="mapId")
    task_power: Optional[str] = Field(None, description="任务电量", alias="taskPower")
    high_battery: Optional[str] = Field(None, description="高电量", alias="highBattery")
    free_time: Optional[str] = Field(None, description="空闲时间", alias="freeTime")
    park_point: Optional[str] = Field(None, description="停车点", alias="parkPoint")
    power_point: Optional[str] = Field(None, description="充电点", alias="powerPoint")
    map_info: Optional[MapInfo] = Field(None, description="地图信息", alias="mapInfo")

    class Config:
        allow_population_by_field_name = True  # 允许通过别名填充字段



# 使用示例
if __name__ == '__main__':
    # 提供的 JSON 数据
    json_data = {
        "code": 200,
        "message": "操作成功",
        "data": {
            "robotId": 10001,
            "robotName": "具身升降双臂机器人",
            "robotNum": "10001",
            "robotMac": "28:B1:33:02:01:2A",
            "robotIp": "192.168.1.126",
            "robotCode": "10001",
            "robotType": "4",
            "isAction": "1",
            "robotDescribe": "自动注册",
            "registUserId": "system",
            "registDate": "2024-08-27T15:01:14",
            "updateUserId": "admin",
            "updateDate": "2025-02-28T17:55:04",
            "mapId": 1,
            "taskPower": "10",
            "highBattery": "20",
            "freeTime": "3",
            "parkPoint": "14",
            "powerPoint": "9",
            "mapInfo": {
                "mapId": 1,
                "mapCode": "10001",
                "mapName": "test",
                "url": "http://192.168.39.135",
                "mapImg": None,
                "mapType": "0",
                "isAction": "1",
                "registUserId": "1",
                "registDate": "2025-03-10T14:04:19",
                "updateUserId": "1",
                "updateDate": "2025-03-10T14:04:19"
            }
        }
    }

    # 提取数据
    robot_data = json_data["data"]

    # 创建 SelectRobotDTO 对象
    robot = SelectRobotDTO(**robot_data)

    # 访问字段
    print("机器人名称:", robot.robot_name)
    print("机器人IP:", robot.robot_ip)
    print("地图信息:", robot.map_info)

    # 检查 URL 是否解析成功
    if robot.map_info and robot.map_info.url:
        url = robot.map_info.url
        if "status=\"failed\"" in url:
            print(f"警告: URL {url} 解析失败。请检查链接的合法性或稍后重试。")
        else:
            print(f"地图 URL: {url}")