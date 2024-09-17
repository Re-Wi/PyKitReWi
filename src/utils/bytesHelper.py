# -*- coding: utf-8 -*-

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