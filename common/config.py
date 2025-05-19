from getmac import get_mac_address

# 产品ID
product_arm_id = "681ac33d6cc0a3de12b50216" # 机械臂产品ID
product_chassis_id = "681ac3336cc0a3de12b50211" # 底盘产品ID
product_camera_id = "681ac3486cc0a3de12b5021b" # 相机产品ID

# 眼睛和机器人眼睛同一个方向
left_arm_ip = "192.168.10.18"
right_arm_ip = "169.254.128.19"
arm_port = 8080
arm_http_port = 8090

# 头部舵机相关
servo_ip = "http://192.168.38.252:8678"
servo_id = 1

# 相机相关
camera_ip = "http://192.168.10.100:5000"

# 底盘相关
#woosh_ip = "http://169.254.128.2:5480"
woosh_ip = "http://192.168.39.135:5480"
woosh_id = 10001
woosh_map = "test"

# 水滴底盘相关
water_ip = "http://192.168.10.10:9001"
water_id = 10001

# IOT ip 端口
# iot_address = "192.168.39.71"
# iot_address = "101.42.154.188"
iot_address = "39.105.185.216"
iot_port = 1883

# IOT 设备id
iot_left_arm = f"{product_arm_id}_{get_mac_address(interface='eth0')}_arm"
iot_right_arm = "67ce3c14a1c868e7b2953bae_right_arm"
iot_left_gripper = "67ce3c14a1c868e7b2953bae_left_gripper"
iot_right_gripper = "67ce3c14a1c868e7b2953bae_right_gripper"
iot_lift = "67ce3c14a1c868e7b2953bae_left_lift"
# iot_woosh = "67d3be5492adf926129737ad_TEST-MAC"
iot_water = f"{product_chassis_id}_{get_mac_address(interface='eth0')}_water"
iot_servo = "67ce3c14a1c868e7b2953bae_servo"
iot_camera = f"{product_camera_id}_{get_mac_address(interface='eth0')}_camera"