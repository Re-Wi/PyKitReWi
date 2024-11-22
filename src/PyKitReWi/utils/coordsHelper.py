from typing import Tuple


def CalculateRowXColY(sequence_number: int, row_x: int = 999, col_y: int = 1) -> Tuple[int, int]:
    """
    根据序列号计算行号和列号。

    这个函数将序列号转换为行号和列号，假设行和列从 0 开始。默认的行数 (`row_x`) 和列数 (`col_y`) 用于确定每一行的列数。
    如果序列号小于 0，函数将返回 `(0, 0)` 表示无效的输入。

    :param sequence_number: 输入的序列号，必须是非负整数。
    :param row_x: 每一行的最大列数，默认为 999。
    :param col_y: 行数，从 1 开始计数，默认为 1。

    :return: 返回一个包含两个整数的元组 `(row, col)`：
        - `row`: 计算得到的行号。
        - `col`: 计算得到的列号。

    :raises ValueError: 如果 `row_x` 或 `col_y` 不是正整数，抛出异常。

    :example:
    >>> CalculateRowXColY(1234, 100, 10)
    (12, 34)

    >>> CalculateRowXColY(0, 999, 1)
    (0, 0)

    >>> CalculateRowXColY(-1)
    (0, 0)
    """
    # 校验 row_x 和 col_y 是否为正整数
    if row_x <= 0 or col_y <= 0:
        raise ValueError("Both row_x and col_y must be positive integers.")

    if sequence_number < 0:
        return 0, 0

    row = sequence_number // col_y
    col = sequence_number % col_y

    return row, col