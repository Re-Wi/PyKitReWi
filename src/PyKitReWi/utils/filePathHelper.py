# -*- coding: utf-8 -*-
"""
File: filePathHelper.py
Author: RejoiceWindow,ReWi
Email: RejoiceWindow@yeah.com
Date: 2024-07-07
Description: ...
Version: 0.0.0
"""

# 版权信息
# Copyright (c) 2024 John Doe. All rights reserved.
# Licensed under the MIT License.

import os
import shutil
from typing import List


def EnsureFolders(path: str) -> str:
    """
    确保文件夹存在，如果不存在则创建该文件夹。

    该函数会检查指定路径的文件夹是否存在。如果不存在，则会创建该文件夹并返回该路径。
    在创建文件夹时，会去除路径首尾的空格，并去除尾部的反斜杠。

    Args:
        path (str): 要确保存在的文件夹路径。

    Returns:
        str: 已创建或已存在的文件夹路径。

    Usage:
        folder_path = EnsureFolders("./data/logs")
        # 确保"./data/logs"文件夹存在，如果不存在则创建。
    """
    # 去除路径两端的空格
    path = path.strip()

    # 去除尾部的反斜杠（在Windows系统中，路径结尾可能带有反斜杠）
    path = path.rstrip("\\")

    # 判断文件夹是否已存在
    if not os.path.exists(path):
        # 如果文件夹不存在，则创建
        os.makedirs(path)
        # 可选：添加日志或打印创建成功的信息
        # print(f"Folder created: {path}")

    return path


def NoDuplicateFile(directory: str, filename: str, file_extension: str = "") -> str:
    """
    创建文件，防止名字重复，自动加序号。

    如果指定的文件名已存在，则会在文件名后附加一个递增的序号，直到找到一个唯一的文件名。

    Args:
        directory (str): 文件所在的目录路径。
        filename (str): 要创建的文件的基本名称（不含扩展名）。
        file_extension (str, optional): 要创建的文件的扩展名（例如：'.db' 或 '.log'）。默认为空。

    Returns:
        str: 新创建文件的完整路径，包括文件名和扩展名。

    Usage:
        new_file_path = NoDuplicateFile("./data", "test_log", ".log")
        # 创建新的日志文件路径，如果已有同名文件，会自动加序号重命名。
    """
    # 生成文件名（如果提供扩展名）
    if len(file_extension) > 0:
        newFilename = filename + file_extension
    else:
        newFilename = filename

    oldFileList = []  # 存储已存在文件的名称
    index = 1  # 文件名索引，从1开始

    # 遍历目录，收集现有的文件名
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            oldFileList.append(file_name)

    # 打印现有文件列表（调试用）
    print(f"{directory}{filename} <oldFileList>: {oldFileList}")

    # 检查文件名是否已存在，如果存在，添加索引
    while index > 0:
        if newFilename in oldFileList:
            # 如果文件名已经存在，添加序号并重试
            print(f"File exists: {os.path.join(directory, newFilename)}")
            newFilename = f"{os.path.basename(filename)}_{index}{os.path.splitext(newFilename)[-1]}"
            print(f"Creating new file: {newFilename}")
            index += 1
        else:
            index = -1  # 找到唯一文件名，结束循环

    # 返回完整的文件路径
    return os.path.join(directory, newFilename)


def Traverse(filepath: str) -> None:
    """
    删除指定路径下的空文件夹和大小为零的文件。

    该函数会递归遍历目录及其子目录，删除所有空文件夹及文件大小为零的文件。

    Args:
        filepath (str): 要遍历的文件夹路径。

    Returns:
        None: 该函数没有返回值，直接对文件夹和文件进行操作。

    Usage:
        Traverse('./data/folder')  # 删除空文件夹和大小为零的文件
    """
    # 获取指定路径下的所有文件和文件夹
    files = os.listdir(filepath)

    for fi in files:
        fi_d = os.path.join(filepath, fi)

        if os.path.isdir(fi_d):  # 如果是文件夹
            if not os.listdir(fi_d):  # 文件夹为空
                os.rmdir(fi_d)  # 删除空文件夹
            else:
                Traverse(fi_d)  # 递归处理子文件夹
        else:
            if os.path.getsize(fi_d) == 0:  # 如果是大小为0的文件
                os.remove(fi_d)  # 删除文件


def MoveAndReplaceFile(source_file: str, destination_folder: str) -> None:
    """
    将源文件移动到目标文件夹，并替换目标文件夹中同名文件（如果存在）。

    Args:
        source_file (str): 要移动的源文件的完整路径。
        destination_folder (str): 目标文件夹路径。

    Returns:
        None: 该函数没有返回值，直接操作文件。

    Usage:
        MoveAndReplaceFile('./source/test.txt', './destination/')
    """
    destination_file = os.path.join(destination_folder, os.path.basename(source_file))

    # 如果目标文件已存在，先删除它
    if os.path.exists(destination_file):
        os.remove(destination_file)

    # 移动源文件到目标文件夹
    shutil.move(source_file, destination_folder)


def GetFilesWithExtension(directory: str, file_extension: str, need_ext: bool = False) -> List[str]:
    """
    获取指定目录下所有具有特定文件后缀的文件名列表。

    Args:
        directory (str): 要搜索的目录路径。
        file_extension (str): 要匹配的文件后缀，如 '.txt'。
        need_ext (bool): 是否需要返回带后缀的文件名。默认为 False，返回去除后缀的文件名。

    Returns:
        List[str]: 匹配的文件名列表。

    Usage:
        GetFilesWithExtension('./data', '.log')  # 获取所有以 .log 结尾的文件名
    """
    # 如果目录不存在，返回空列表
    if not os.path.exists(directory):
        return []

    # 获取目录下所有文件
    all_files = os.listdir(directory)

    # 根据 need_ext 过滤文件
    if need_ext:
        return [file for file in all_files if file.endswith(file_extension)]
    else:
        return [file.rstrip(file_extension) for file in all_files if file.endswith(file_extension)]


def GetFileFullPath(path: str) -> str:
    """
    获取文件的完整路径。兼容相对路径和绝对路径，判断文件是否存在。

    Args:
        path (str): 要检查的文件路径。

    Returns:
        str: 如果文件存在，返回文件的绝对路径；否则返回空字符串。

    Usage:
        GetFileFullPath('./test.txt')  # 获取相对路径文件的完整路径
    """
    if os.path.isfile(path):
        return os.path.abspath(path)
    return ""


def CheckFile(filepath: str, expected_type: str) -> bool:
    """
    检查给定文件路径的文件类型是否与期望类型匹配，并判断文件是否存在。

    Args:
        filepath (str): 文件路径。
        expected_type (str): 期望的文件类型，支持 'image'、'video'、'log' 等。

    Returns:
        bool: 如果文件存在且类型匹配，返回 True；否则返回 False。

    Raises:
        ValueError: 如果提供的期望类型不在预定义类型列表中，抛出异常。

    Usage:
        CheckFile('./image.png', 'image')  # 检查文件是否为图片类型
    """
    # 定义支持的文件类型及其对应的扩展名
    type_extensions = {
        'image': ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'),
        'video': ('.mp4', '.avi', '.mov', '.mkv', '.flv'),
        'log': ('.log', '.txt')
    }

    # 检查文件是否存在
    if not os.path.isfile(filepath):
        print(f"File '{filepath}' does not exist.")
        return False

    # 获取文件扩展名
    _, ext = os.path.splitext(filepath)

    # 获取期望类型的扩展名列表
    expected_extensions = type_extensions.get(expected_type.lower(), None)

    if expected_extensions is None:
        raise ValueError(f"Unknown expected type: {expected_type}")

    # 检查文件扩展名是否与期望类型匹配
    return ext.lower() in expected_extensions
