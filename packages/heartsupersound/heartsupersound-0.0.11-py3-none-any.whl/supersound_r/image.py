"""此文件包含和图像有关的函数"""
import cv2
import numpy as np

def image_to_millimeter(image_path, threshold=0, pixel_spacing_x=0.119, pixel_spacing_y=0.119, origin_x=948,
                        origin_y=38,
                        x_direction=1, y_direction=1):
    """
    Function:
        找出图中大于某一阈值的像素点，并将其转化为毫米坐标系，
    输入：
        image_path:图像的地址
        threshold：像素阈值
        pixel_spacing_x：X轴像素和mm的转换
        pixel_spacing_y：Y轴像素和mm的转换

        origin_x,origin_y：超声探头在图像中的位置，将此点作为坐标原点
        x_direction,y_direction:方向向量
    返回：
        图像的毫米坐标系
    """
    # 加载图像
    image = cv2.imread(image_path, 0)
    img_point = np.where(image > threshold)  # 找到图像中大于0的坐标
    x_coords = []
    y_coords = []
    for p in range(len(img_point[0])):
        x = img_point[0][p]
        y = img_point[1][p]
        # 创建与图像分辨率相同的网格坐标
        x_coords.append((x - origin_x) * pixel_spacing_x * x_direction)
        y_coords.append((y - origin_y) * pixel_spacing_y * y_direction)
    position_mm = np.dstack((x_coords, y_coords))[0]
    return position_mm
def points_to_millimeter(img_point, pixel_spacing_x=0.119, pixel_spacing_y=0.119, origin_x=948, origin_y=38):
    """
    功能：
        将二维点云设置为毫米坐标系
    输入：
        img_point：二维像素点坐标值(x,y)，这些点的坐标必须来自于超声图像（经过像素阈值法保留的图像坐标位置）
        pixel_spacing_x，pixel_spacing_y：设置点云间的的Pixel Spacing，即将图像的像素映射到毫米(mm)坐标系中
        origin_x，origin_y：将点云的原点设置为“超声探头在图像中的位置（948，38)

    返回：
        以毫米坐标系为单位，以超声探头为原点的图像上各个像素点的坐标位置
    """
    x_coords = []
    y_coords = []
    z_coords = []
    for p in range(len(img_point)):
        x = img_point[p][0]
        y = -img_point[p][1]
        z = 0
        # 创建与图像分辨率相同的网格坐标
        x_coords.append((x - origin_x) * pixel_spacing_x)
        y_coords.append((y + origin_y) * pixel_spacing_y)
        z_coords.append(z)
    result = np.dstack((x_coords, y_coords, z_coords))[0]
    return result

def get_point_threshold(img, pixel_threshold=0, line_space=50):
    """
    功能：
    获取图像中的像素点大于某一阈值的坐标

    参数：
    img:图像,灰度图
    line_space:扫面的间隔，最小为1行
    pixel_threshold:像素阈值

    返回：
    img_postion=[[ALL_X], [ALL_Y]]
    """
    k = 0
    # 隔行扫描，归零
    while k < img.shape[0]:
        try:
            img[k + 1:k + line_space, :] = 0
        except:
            img[k + 1:, :] = 0
        k += line_space
    local = np.where(img > pixel_threshold)  # 像素值大于阈值保留
    img_postion = [local[1], local[0]]
    img_postion_xy = np.dstack((img_postion[0], img_postion[1]))[0]
    return img_postion_xy

def read_and_clear_image(image_path, label_image_path):
    """清除图片杂质"""
    image = cv2.imread(image_path, 0)
    mask_image = cv2.imread(label_image_path, 0)
    new_image = cv2.bitwise_and(image, image, mask=mask_image)
    return new_image
def read_image(image_path, model=0):
    """清除图片杂质"""
    image = cv2.imread(image_path, model)
    return image
def plot_contours(image, label_image_path):
    """将图片边缘描绘出来
    image:原图像
    label_image_path：需要是这张图片的边界
    """
    # 将 mask_image 转换为三通道
    mask_image_3channel = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    edge_image = cv2.imread(label_image_path, 0)
    # 创建具有3个通道的图像
    green_channel = cv2.merge((np.zeros_like(edge_image), edge_image, np.zeros_like(edge_image)))
    # 图像叠加
    contours_image = cv2.addWeighted(mask_image_3channel, 1, green_channel, 0.7, 0)
    return contours_image


def get_boundary(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except:
        gray = np.asarray(image)
    # 二值化掩膜图像
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

    # 寻找最外层轮廓
    """
    mode:轮廓检索模式
    RETR_EXTERNAL ：只检索最外面的轮廓；
    RETR_LIST：检索所有的轮廓，并将其保存到一条链表当中；
    RETR_CCOMP：检索所有的轮廓，并将他们组织为两层：顶层是各部分的外部边界，第二层是空洞的边界;
    RETR_TREE（最常用）：检索所有的轮廓，并重构嵌套轮廓的整个层次;
    method:轮廓逼近方法
    CHAIN_APPROX_NONE：以Freeman链码的方式输出轮廓，所有其他方法输出多边形（顶点的序列）。
    CHAIN_APPROX_SIMPLE（最常用）:压缩水平的、垂直的和斜的部分，也就是，函数只保留他们的终点部分。
    """
    contours, hierarchy = cv2.findContours(image=binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个空白图像来绘制最外层轮廓
    contour_image = np.zeros_like(image)

    # 绘制最外层轮廓
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 3)
    return contour_image

