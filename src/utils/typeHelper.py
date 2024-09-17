from typing import Any, List, Type


def CheckListOfElementType(value: Any, expected_type: Type) -> bool:
    """
    判断变量是否是包含指定类型元素的列表。

    这个函数检查给定的变量是否是一个列表，并且该列表中的所有元素都属于指定的类型。如果变量不是列表，函数将返回 False。

    :param value: 需要检查的变量，可以是任何类型。
    :param expected_type: 期望的元素类型。用于验证列表中每个元素的类型。

    :return: 如果变量是包含指定类型元素的列表，返回 True；否则返回 False。

    :example:
        >>> CheckListOfElementType([1, 2, 3], int)
        True

        >>> CheckListOfElementType(["1", "2", "3"], int)
        False

        >>> CheckListOfElementType(["1", "2", "3"], str)
        True
    """
    if isinstance(value, list):
        return all(isinstance(item, expected_type) for item in value)
    return False
