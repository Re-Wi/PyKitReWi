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


def Traverse(filepath):
    """
    删除空文件夹，否则会报错
    :param filepath:
    :return:
    """
    # 遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):  # 判断是否为文件夹
            if not os.listdir(fi_d):  # 如果文件夹为空
                os.rmdir(fi_d)  # 删除这个空文件夹
            else:
                Traverse(fi_d)
        else:
            # file = os.path.join(filepath, fi_d) #重复加入路径，报错
            if os.path.getsize(fi_d) == 0:  # 文件大小为0
                os.remove(fi_d)  # 删除这个文件


def EnsureFolders(path):
    """
    确保文件夹存在，不存在则创建
    :param path:
    :return:
    """
    # 去除首尾的空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        # print(path+' 创建成功')
    return path


def NoDuplicateFile(filepath, filename, file_extension=""):
    '''
    创建文件，防止名字重复，自动加序号

    :param filepath: 文件所在的目录路径
    :param filename: 要创建的文件的基本名称
    :param file_extension: 要创建的文件的后缀（例如：'.db' 或 '.log'）
    :return: 新创建文件的完整路径
    '''
    if len(file_extension) > 0:
        newFilename = filename + file_extension
    else:
        newFilename = filename
    oldFileList = []
    index = 1

    # 遍历目录
    for root, dirs, files in os.walk(filepath):
        # 获取文件名称及路径
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)
            # 将文件名添加到列表
            oldFileList.append(file_name)

    print(filepath + filename + ' <oldFileList>:', oldFileList)

    while index > 0:
        if newFilename in oldFileList:
            # 如果文件名已经存在，添加序号并重试
            print('Get it', os.path.join(filepath, newFilename))
            newFilename = f"{os.path.basename(filename)}_{index}{os.path.splitext(newFilename)[-1]}"
            print('Create a new file:', newFilename)
            index += 1
        else:
            index = -1

    return os.path.join(filepath, newFilename)


def MoveAndReplaceFile(source_file, destination_folder):
    """
    将源文件移动到目标文件夹，并替换目标文件夹中同名文件（如果存在）。

    :param source_file: 要移动的源文件的完整路径
    :param destination_folder: 目标文件夹的路径
    """
    # 目标文件的完整路径
    destination_file = os.path.join(destination_folder, os.path.basename(source_file))

    # 如果目标文件已经存在，删除它
    if os.path.exists(destination_file):
        os.remove(destination_file)

    # 使用shutil.move函数移动文件（可能会覆盖目标文件）
    shutil.move(source_file, destination_folder)


def GetFilesWithExtension(directory, file_extension, need_ext=False):
    """
    获取指定目录下所有具有特定文件后缀的文件名列表。

    :param directory: 要搜索的目录路径
    :param file_extension: 目标文件的后缀（例如：'.txt'）
    :return: 包含匹配文件名的列表
    """
    # 确保目录存在
    if not os.path.exists(directory):
        return []

    # 获取目录下所有文件
    all_files = os.listdir(directory)
    # 使用列表推导式过滤具有指定后缀的文件
    if need_ext:
        filtered_files = [file for file in all_files if file.endswith(file_extension)]
    else:
        filtered_files = [file.rstrip(file_extension) for file in all_files if file.endswith(file_extension)]
    # 返回匹配文件名的列表
    return filtered_files


def GetFileFullPath(path):
    """
    兼容相对路径和绝对路径，判断文件是否存在，存在则返回完整路径
    :param path: 相对或绝对路径
    :return: 文件存在时返回完整路径，否则返回 None
    """
    if os.path.isfile(path):
        return os.path.abspath(path)
    return ""


def CheckFile(filepath: str, expected_type: str) -> bool:
    """
    检查给定文件路径的文件类型是否与期望类型匹配，并判断文件是否存在于文件系统中。

    :param filepath: 文件的路径。
    :param expected_type: 期望的文件类型，可以是 'image'、'video'、'log' 等。

    :return: 如果文件存在且类型与期望匹配，则返回 True；否则返回 False。
    :raises ValueError: 如果提供的期望类型不在预定义类型列表中，则抛出异常。
    """
    # 检查文件是否存在
    if not os.path.isfile(filepath):
        print(f"File '{filepath}' does not exist.")
        return False

    # 定义文件扩展名与文件类型的映射
    type_extensions = {
        'image': ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'),
        'video': ('.mp4', '.avi', '.mov', '.mkv', '.flv'),
        'log': ('.log', '.txt')
    }

    # 获取文件的扩展名
    _, ext = os.path.splitext(filepath)

    # 获取期望的文件扩展名列表
    expected_extensions = type_extensions.get(expected_type.lower(), None)

    if expected_extensions is None:
        raise ValueError(f"Unknown expected type: {expected_type}")

    # 检查文件扩展名是否匹配
    return ext.lower() in expected_extensions


# 程序入口
if __name__ == "__main__":
    # 示例用法
    filepath = 'directory'
    filename = 'example'
    file_extension_db = '.db'
    file_extension_log = '.log'

    # 创建不重复的数据库文件
    new_db_file = NoDuplicateFile(filepath, filename, file_extension_db)
    print(f"New database file created: {new_db_file}")

    # 创建不重复的日志文件
    new_log_file = NoDuplicateFile(filepath, filename, file_extension_log)
    print(f"New log file created: {new_log_file}")
    # 示例用法
    source_file = 'path/to/source/file.ext'
    destination_folder = 'path/to/destination/'

    MoveAndReplaceFile(source_file, destination_folder)

    # 示例用法
    directory_path = '../data/script'
    file_extension = '.txt'

    result = GetFilesWithExtension(directory_path, file_extension)

    if result is not None:
        print(f"在目录 {directory_path} 下找到以下 {file_extension} 文件:")
        for file_name in result:
            print(file_name)
    else:
        print(f"目录 {directory_path} 不存在.")
