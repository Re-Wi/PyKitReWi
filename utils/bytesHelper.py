# -*- coding: utf-8 -*-
import binascii

from loguru import logger


def SliceBytesSafe(data, positions):
    """
    将 bytes 对象根据给定的起始和结束位置列表切片，并保存为一个数组。

    参数：
    - data: 要切片的 bytes 对象。
    - positions: 包含起始和结束位置元组的列表。

    返回：
    - 保存切片结果的数组。
    """
    result_array = []
    data_length = len(data)

    for start, end in positions:
        # 检查起始和结束位置是否在合法范围内
        if 0 <= start < data_length and 0 <= end <= data_length and start < end:
            # 切片并添加到结果数组
            sliced_bytes = data[start:end]
            result_array.append(sliced_bytes)
        else:
            # 如果位置不合法，打印消息并忽略该位置
            print(f"Illegal position: ({start}, {end}). Ignoring.")

    return result_array


################# start >>> int_to_lsb_msb:function <<< start #################
def int_to_lsb_msb(num: int):
    """
    :param num:int
    :return: lsb, msb
    """
    lsb = num & 0xFF  # 获取最低字节
    msb = (num >> 8) & 0xFF  # 获取次低字节
    return lsb, msb


################# end >>> int_to_lsb_msb:function <<< end #################
################# start >>> BytesToHexPrint:function <<< start #################
def BytesToHexPrint(dataObj, expectData=""):
    # 使用hexlify函数将bytes数据转换为16进制字符串
    hex_string = binascii.hexlify(dataObj).decode('utf-8').upper()
    # 插入空格
    dataObj = ' '.join(hex_string[i:i + 2] for i in range(0, len(hex_string), 2))
    # expectData = optionsDict.get('expectData', '').strip()
    if len(expectData) <= 0:
        logger.info(dataObj)
        return True
    elif str(expectData) in str(dataObj):
        logger.success(dataObj)
        return True
    else:
        logger.error(dataObj)
        return False


################# end >>> BytesToHexPrint:function <<< end #################

# 程序入口
if __name__ == '__main__':
    # 示例使用
    my_bytes = b"0123456789"
    # 多个起始和结束位置的列表，包括一个非法位置
    positions_list = [(0, 2), (2, 5), (5, 8), (8, 10), (11, 15)]
    # 切片并保存为数组，同时处理非法位置
    result_array = SliceBytesSafe(my_bytes, positions_list)
    # 打印结果
    print(result_array)
