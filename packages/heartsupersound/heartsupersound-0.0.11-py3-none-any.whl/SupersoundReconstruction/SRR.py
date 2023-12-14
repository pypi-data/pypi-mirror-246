"""包含和旋转有关的函数"""
import numpy as np
import math

def quaternion_to_matrix(input):
    """
    四元素转旋转矩阵
    输入：四元素[Q0,Qx,Qy,Qz]
    输出：旋转矩阵R
    """
    Q0, Qx, Qy, Qz = input[0], input[1], input[2], input[3]
    # ************************************说明书提供计算旋转矩阵的元素************************************
    R00 = (Q0 * Q0) + (Qx * Qx) - (Qy * Qy) - (Qz * Qz)
    R01 = 2 * ((Qx * Qy) - (Q0 * Qz))
    R02 = 2 * ((Qx * Qz) + (Q0 * Qy))
    R10 = 2 * ((Qx * Qy) + (Q0 * Qz))
    R11 = (Q0 * Q0) - (Qx * Qx) + (Qy * Qy) - (Qz * Qz)
    R12 = 2 * ((Qy * Qz) - (Q0 * Qx))
    R20 = 2 * ((Qx * Qz) - (Q0 * Qy))
    R21 = 2 * ((Qy * Qz) + (Q0 * Qx))
    R22 = (Q0 * Q0) - (Qx * Qx) - (Qy * Qy) + (Qz * Qz)
    R = np.array([[R00, R01, R02], [R10, R11, R12], [R20, R21, R22]])
    return R

def quaternion_to_euler(q):
    """
    四元数转欧拉角
    输入：四元素[Q0,Qx,Qy,Qz]
    输出：欧拉角[roll,pitch,yaw]
    Example:
        q = [0.0046, 0.8009, -0.5988, -0.0074]
        Euler2R, Euler2D = quaternion_to_euler(q)
        print("欧拉角转旋转矩阵Rad弧度制：", Euler2R)
        print("欧拉角转旋转矩阵角度制Deg：", Euler2D)
    """
    q0, q1, q2, q3 = q[0], q[1], q[2], q[3]

    roll = math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2))
    pitch = math.asin(2 * (q0 * q2 - q3 * q1))
    yaw = math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3))
    Euler2Rad = [roll, pitch, yaw]# 弧度制
    Euler2Degrees = [math.degrees(i) for i in Euler2Rad]# 角度制
    return Euler2Rad, Euler2Degrees

def euler_to_matrix(Rad):
    """
    欧拉角转旋转矩阵
    输入：Rad = [roll，pitch，yaw]分别表示物体绕,x,y,z的旋转角度,注意是弧度制
    输出：旋转矩阵
    Example:
        degrees = [179.07014553339246, 0.36350749032360136, -73.57515363014724]
        print("欧拉角为(角度制)：\n", degrees)
        Rad = [math.radians(i) for i in degrees]
        print("欧拉角为(弧度制)：\n",Rad)
        Euler2R = Euler2Matrix(Rad)
        print("旋转矩阵为：\n", Euler2R)
    """
    roll, pitch, yaw = Rad[0], Rad[1], Rad[2]
    Rx = np.array(
        [[1, 0, 0], [0, np.cos(roll), -np.sin(roll)], [0, np.sin(roll), np.cos(roll)]])
    Ry = np.array(
        [[np.cos(pitch), 0, np.sin(pitch)], [0, 1, 0], [-np.sin(pitch), 0, np.cos(pitch)]])
    Rz = np.array(
        [[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])

    # 计算最终旋转矩阵
    R = np.dot(Rz, np.dot(Ry, Rx))
    return R
def matrix_to_euler(rot_matrix, rotation_order='XYZ'):
    """
    旋转矩阵转欧拉角，完全计算实现
    输入：
    rot_matrix：3×3的矩阵
    输出：
    xyz三个方向的旋转角
    Example:
        transposed_rotation_matrix = np.array(
        [[0.08516241, - 0.97070625, - 0.22467317],
         [-0.76330659, 0.08136997, - 0.64089255],
         [0.64039964, 0.22607432, - 0.73401634]])
        euler_angles = rotation_matrix_to_euler_angles(transposed_rotation_matrix)
        print(euler_angles)
    """
    if rotation_order != 'XYZ':
        raise ValueError("目前只支持 XYZ 旋转顺序")

    r11, r12, r13 = rot_matrix[0]
    r21, r22, r23 = rot_matrix[1]
    r31, r32, r33 = rot_matrix[2]

    theta_x = math.atan2(r32, r33)
    theta_y = math.atan2(-r31, math.sqrt(r32 ** 2 + r33 ** 2))
    theta_z = math.atan2(r21, r11)

    theta_x = math.degrees(theta_x)
    theta_y = math.degrees(theta_y)
    theta_z = math.degrees(theta_z)

    return [theta_x, theta_y, theta_z]


def cloud_rotate_around_point(point_cloud, quats, center=[0, 0, 0]):
    """
    功能：将点云围绕某一个原点进行旋转
    :param point_cloud:输入点云[[x1,y1,z1],[x2,y2,z2],...]
    :param quats:四元素[q1,q2,q3,q4]
    :param center:旋转中心[x,y,z]
    :return:旋转后的点云[[x'1,y'1,z'1],[x'2,y'2,z'2],...]
    """
    Euler2Rad, Euler2Degrees = quaternion_to_euler(quats)
    rotation = euler_to_matrix(Euler2Rad)
    # 将点云中的点移到旋转中心
    centered_points = point_cloud - center
    # 进行旋转
    rotated_points = np.dot(centered_points, rotation.T)  # 转置矩阵以进行矩阵乘法
    # 将点云移回原始位置
    rotated_points = rotated_points + center

    return rotated_points

def cloud_translate(point_cloud, xyz_pos):
    """
    功能：平移矩阵
    :param point_cloud:输入点云[[x1,y1,z1],[x2,y2,z2],...]
    :param xyz_pos:点云平移量[tx,ty,tz]
    :return:旋转后的点云[[x'1,y'1,z'1],[x'2,y'2,z'2],...]
    """
    translate_points = point_cloud + xyz_pos
    return translate_points