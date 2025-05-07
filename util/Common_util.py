import math
import cv2
import subprocess
import platform
import base64
import socket
import uuid


def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print(f"获取 IP 地址失败: {e}")
        return None


def get_mac_address():
    try:
        mac_address = uuid.getnode()
        mac_address = ':'.join(['{:02x}'.format((mac_address >> i) & 0xff) for i in range(0, 2 * 6, 2)][::-1])
        return mac_address
    except Exception as e:
        print(f"获取 MAC 地址失败: {e}")
        return None


def calculate_distances(tcp_pose_target, tcp_pose_cur):
    """
    分别计算两个三维坐标点在 x、y、z 轴上的距离，以及直线距离
    :param tcp_pos_target: 目标点的 XYZ 坐标
    :param tcp_pos_cur: 当前点的 XYZ 坐标
    :return: x、y、z、直线 距离
    """
    x1, y1, z1 = tcp_pose_target[:3]
    x2, y2, z2 = tcp_pose_cur[:3]
    distance_x = abs(x2 - x1)
    distance_y = abs(y2 - y1)
    distance_z = abs(z2 - z1)
    distance_line = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

    # 保留6位小数
    distance_x = round(distance_x, 6)
    distance_y = round(distance_y, 6)
    distance_z = round(distance_z, 6)
    distance_line = round(distance_line, 6)

    print(f"距离计算： x={distance_x}, y={distance_y}, z={distance_z}, line={distance_line}")
    return [distance_x, distance_y, distance_z, distance_line]


def getImgBase64(img_path) -> str:
    '''
    将图片变成base64进行传输
    :param img_path: 图片路径
    :return: img_base64
    '''
    img = cv2.imread(img_path)
    if img is None:
        print("无法读取图像，请检查路径是否正确")
        return
    _, img_encoded = cv2.imencode('.jpg', img)  # 转换为 JPEG 格式
    img_bytes = img_encoded.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return img_base64


def ping_ip(ip):
    try:
        if platform.system().lower() == "windows":
            output = subprocess.run(
                ["ping", "-n", "1", "-w", "500", ip],  # 设置超时时间为500毫秒
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        return output.returncode == 0
    except Exception as e:
        return False


def scan_network(start_ip, end_ip):
    ips = []
    print(f"扫描 IP: 192.168.39.{start_ip} to 192.168.39.{end_ip}")
    for i in range(start_ip, end_ip + 1):
        ip = f"192.168.39.{i}"
        if ping_ip(ip):
            ips.append(ip)
            print(f"IP {ip} ✔======")
        else:
            print(f"IP {ip} ×")
    print(ips)

if __name__ == '__main__':
    print(f"当前电脑mac: {get_mac_address()}")