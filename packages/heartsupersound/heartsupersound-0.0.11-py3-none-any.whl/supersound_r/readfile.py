"""此文件包换和读取有关的函数"""
import json
import os
def read_record(record_path):
    """
    功能：
        读取.record文件
    输入：
        采集图片的保存路径；一个周期的图片数量
    返回：
        图片和角度信息
        """
    with open(record_path, 'r', encoding='utf-8') as f:
        image_angle = []
        for ann in f.readlines():
            ann = ann.strip('\n')  # 去除文本中的换行符
            image_angle.append(ann)
    dir_a = {}
    dir_b = {}
    for i in image_angle[11:len(image_angle)]:
        key_list = i.split('; ')[0:-1]
        key_part0 = key_list[0].split(', ')
        key_part1 = key_list[1].split(', ')
        # 将字符串数字列表转换为浮点数列表

        if key_part1[0] == '0x000a':
            q_a = [float(item) for item in key_part1[2:6]]
            xyz_a = [float(item) for item in key_part1[6:9]]
            dir_a.update({key_part0[0]: [q_a, xyz_a]})
        try:
            key_part2 = key_list[2].split(', ')
            if key_part2[0] == '0x000b':
                q_b = [float(item) for item in key_part2[2:6]]
                xyz_b = [float(item) for item in key_part2[6:9]]
                dir_b.update({key_part0[0]: [q_b, xyz_b]})
        except:
            pass
    return dir_a, dir_b
def read_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_format_file_list(path, format='.json'):
    file_name_list = os.listdir(path)
    file_list = []
    for f in file_name_list:
        if f.endswith(format):
            file_list.append(os.path.join(path, f))
    return file_list