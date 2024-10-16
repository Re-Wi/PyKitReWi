# -*- coding: utf-8 -*-
import random
import re
import string


def ProcessMSToHHMMSS(milliseconds):
    seconds = milliseconds / 1000
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


def parse_bit_flags(bit_string, flag_descriptions):
    """将二进制字符串转换为描述字符串列表"""
    flags = []
    for idx, bit in enumerate(bit_string[::-1]):  # 逆序遍历
        if bit == '1':
            flags.append(flag_descriptions[idx])
    return flags


def convert_hex_to_voltage(hex_str):
    """将十六进制字符串转换为电压值"""
    return f"{round((int(hex_str, 16) * 1 * 3.3 * 11) / 4096, 2)}V ({int(hex_str, 16)})"


def format_system_time(hex_str):
    """将十六进制字符串转换为系统时间"""
    return f"{ProcessMSToHHMMSS(int(hex_str, 16))} ({int(hex_str, 16)}ms)"


def append_or_blank(old_values: list, new_value, obj_text, listData, filter=False):
    """如果new_value在old_values中，添加空格，否则添加new_value"""
    if new_value in old_values[0]:
        listData.append(None)
    else:
        listData.append(obj_text)
        if filter:
            old_values[0] = new_value


kAdcTempTab = [
    3896, 3885, 3873, 3862, 3849, 3836, 3823, 3809,
    3794, 3779, 3763, 3747, 3730, 3712, 3694, 3675,
    3656, 3636, 3615, 3594, 3572, 3549, 3526, 3502,
    3477, 3452, 3426, 3399, 3372, 3344, 3315, 3286,
    3256, 3225, 3194, 3162, 3130, 3097, 3063, 3029,
    2995, 2960, 2925, 2889, 2853, 2816, 2779, 2742,
    2704, 2667, 2629, 2590, 2552, 2513, 2474, 2435,
    2396, 2357, 2318, 2279, 2240, 2202, 2163, 2124,
    2086, 2048, 2009, 1971, 1934, 1896, 1859, 1822,
    1786, 1750, 1714, 1679, 1644, 1609, 1575, 1542,
    1509, 1476, 1444, 1412, 1381, 1350, 1319, 1290,
    1260, 1232, 1203, 1175, 1148, 1121, 1095, 1070,
    1044, 1020, 995, 972, 948, 926, 904, 883,
    862, 841, 821, 802, 783, 764, 746, 728,
    711, 694, 677, 661, 645, 630, 615, 600,
    586, 572, 558, 545, 532, 519, 495, 483,
    483, 472, 461, 450, 439, 429, 419, 409,
    399, 390, 381, 372, 363, 355, 347, 339,
    331, 324, 316, 309, 302, 295, 289, 282,
    276, 270, 264, 258, 252, 246, 241, 236,
    230, 225, 221, 216, 211, 207
]


def CtApPowerAdcToTemperature(adcValue):
    ret = 0
    left, right, mid = 0, 0, 0
    pTab = kAdcTempTab

    if adcValue >= pTab[0]:
        ret = -40
    elif adcValue <= pTab[-1]:
        mid = len(pTab) - 1 - 40
        ret = mid
    else:
        left = 0
        right = len(pTab) - 1

        while left < right:
            mid = (left + right) // 2

            if adcValue == pTab[mid]:
                break
            elif adcValue < pTab[mid] and adcValue > pTab[mid + 1]:
                mid = mid if (pTab[mid] - adcValue) < (adcValue - pTab[mid + 1]) else (mid + 1)
                break
            else:
                if adcValue > pTab[mid]:
                    right = mid
                else:
                    left = mid

        ret = mid - 40

    return ret


def convert_hex_to_temperature(hex_str):
    """将十六进制字符串转换为温度值"""
    return f"{CtApPowerAdcToTemperature(int(hex_str, 16) - 40)} °C ({hex_str})"


def extract_window_classes(file_path):
    # 读取文件内容
    with open(file_path, 'r') as file:
        file_content = file.read()

    # 正则表达式匹配带 Window 后缀的类名，仅从 import 语句中提取
    pattern = r'from\s+\.(\w+)\s+import\s+(\w*Window)\b'
    matches = re.findall(pattern, file_content)

    # 返回匹配到的模块名和类名
    return matches


def ToUpperCamelCase(input_string):
    """
    转为大驼峰命名法
    :param input_string:
    :return:
    """
    words = input_string.split('_')  # 以下划线拆分字符串为单词
    camel_case_words = [word[0].upper() + word[1:] for word in words]  # 手动将每个单词的首字母大写
    return ''.join(camel_case_words)  # 连接单词，得到大驼峰字符串


def FirstLetterToLower(input_string: str):
    """
    首字母小写
    :param input_string:
    :return:
    """
    if len(input_string) > 0:
        return input_string[0].lower() + input_string[1:]
    else:
        return input_string


def FirstLetterToUpper(input_string: str):
    """
    首字母大写
    :param input_string:
    :return:
    """
    if len(input_string) > 0:
        return input_string[0].upper() + input_string[1:]
    else:
        return input_string


def GenerateRandomString(length):
    # 定义包含所有可能字符的字符集
    characters = string.ascii_letters + string.digits + string.punctuation

    # 使用 random 模块生成随机字符
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


################# start >>> hex_string_to_list:function <<< start #################
def hex_string_to_list(hex_string):
    """
    将以空格分隔的十六进制字符串转换为整数列表。
    :param hex_string:
    :return:
    """
    hex_values = hex_string.split()  # 通过空格拆分字符串并生成十六进制值的列表
    # print("len：", len(hex_values))
    result = [int(hex_value, 16) for hex_value in hex_values]  # 将每个十六进制值转换为整数
    return result


################# end >>> hex_string_to_list:function <<< end #################

# 程序入口
if __name__ == '__main__':
    pass
