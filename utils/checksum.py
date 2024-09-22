# -*- coding: UTF-8 -*-
# coding=utf-8
# 在循环内部，它将 pData 指针移动到下一个字节，然后使用异或操作（^）更新校验和。这是一种常见的校验和计算方法，它将每个字节与先前计算的校验和进行异或操作，以逐渐积累校验和值。
# 最后，函数返回计算得到的校验和。
# /**
#  * @brief calculate and return i2c0 checksum
#  * @param pData data pointer
#  * @param length data length
#  * @return uint8 checksum
#  */
def i2c0_get_checksum(data):
    checksum = data[0]  # 初始化校验和为数据的第一个字节
    for i in range(len(data) - 1):
        checksum ^= data[i + 1]  # 使用异或操作更新校验和
    return checksum & 0xFF  # 返回计算得到的校验和 低8位结果


# def get_tcon_checksum(data):
#     checksum = data[0]  # 初始化校验和为数据的第一个字节
#     for i in range(len(data) - 1):
#         checksum += data[i + 1] #直接相加
#     return checksum  # 返回计算得到的校验和

def get_tcon_checksum(data):
    checksum = data[0] & 0xFF  # 初始化校验和为数据的第一个字节的低8位
    for byte in data[1:]:
        checksum += byte & 0xFF  # 将每个字节的低8位加到校验和中
    return checksum & 0xFF  # 返回校验和的低8位结果


def hex_string_to_list(hex_string):
    """
    将以空格分隔的十六进制字符串转换为整数列表。

    Args:
        hex_string (str): 包含十六进制值的字符串，各值之间用空格分隔。

    Returns:
        list: 包含整数值的列表。

    Example:
        >>> hex_string = "22 00 03 02 50"
        >>> hex_list = hex_string_to_list(hex_string)
        >>> print(hex_list)
        [34, 0, 3, 2, 80]
    """
    hex_values = hex_string.split()  # 通过空格拆分字符串并生成十六进制值的列表
    print("len：", len(hex_values))
    result = [int(hex_value, 16) for hex_value in hex_values]  # 将每个十六进制值转换为整数
    return result


# "Checksum: 0x{result:02X}" 是格式化字符串的内容。在大括号 {} 内，result 表示要格式化的变量，02X 是格式化说明符，它的含义如下：
# 0 表示使用零来填充不足的位置。
# 2 表示至少使用两个字符的宽度。
# X 表示以大写十六进制表示。
if __name__ == "__main__":
    # 输入数据，以列表形式表示
    # originalData = "22 00 03 02 50"
    # hexListData = [0x22, 0x00, 0x03, 0x02, 50]
    originalData = "7A 01 04 00 00 5A 00"
    intListData = hex_string_to_list(originalData)
    # print(intListData)
    # 调用计算函数并获取校验和
    result = i2c0_get_checksum(intListData)
    # 打印结果
    print(f"i2c0_get_checksum -> Checksum: 0x{result:02X}")
    # 调用计算函数并获取校验和
    result = get_tcon_checksum(intListData)
    # 打印结果
    print(f"get_tcon_checksum -> Checksum: 0x{result:02X}")

# 使用计算器
# "AND" 表示与运算，只有当两个操作数都为真时结果为真。
# "OR" 表示或运算，只要有一个操作数为真，结果就为真。
# "NOT" 表示非运算，它是一个一元运算，用于反转操作数的值。
# "NAND" 表示与非运算，是与运算的否定。结果为真除非两个操作数都为真。
# "NOR" 表示或非运算，是或运算的否定。结果为真只有当两个操作数都为假。
# "XOR" 表示异或运算，其结果如前面所述。
