# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 23:28:00 2019

@author: 1
"""
from .filePathHelper import Traverse
import os


class PicturesHandler:
    file_paths = []  # 文件列表
    file_index = 0  # 文件索引
    image_dict = {}  # 指令显示图片，查找字典，用索引值（图片名第一个_之前的整数值）

    # 导入文件夹
    def OpenDirectory(self, picturesPath='', filenameSplit='D-'):
        # cur_dir = QDir.currentPath()  # 获取当前文件夹路径
        # 删除空文件夹
        Traverse(picturesPath)
        # 选择文件夹
        # dir_path = QFileDialog.getExistingDirectory(None,'打开文件夹',r'../data/pictures/')
        # 读取文件夹文件
        self.file_paths.clear()
        for root, dirs, files in os.walk(picturesPath, topdown=False):
            for file in files:
                if file.lower().endswith(
                        ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                    img_path = os.path.join(root, file)
                    self.file_paths.append(img_path)
                    idx = (file.split(filenameSplit)[1]).split('.')[0]
                    self.image_dict[int(idx)] = img_path
        # print('image_dict', self.image_dict)
        if len(self.file_paths) <= 0:
            return None
        # 获取第一个文件
        self.file_index = 0
        self.file_paths = sorted(self.file_paths, key=str.lower)
        # 处理文件
        # self.ProcessImage(cur_path)
        return self.file_paths

    # 通过字典获取图片
    def FileCurrentByDict(self, fileIndex=0):
        cur_path = self.image_dict.get(fileIndex)
        if cur_path:
            return cur_path

    # 通过文件列表获取某个文件
    def FileCurrentByList(self, fileIndex=None):
        if not fileIndex == None:
            self.file_index = fileIndex
        if self.file_index >= len(self.file_paths):
            self.file_index = len(self.file_paths) - 1
        elif self.file_index < 0:
            self.file_index = 0
        if len(self.file_paths) <= 0 or self.file_index >= len(self.file_paths):
            return None
        cur_path = self.file_paths[self.file_index]
        # self.ProcessImage(cur_path)
        return cur_path

    # 下一个文件
    def FileNext(self):
        # 文件索引累加 1
        self.file_index += 1
        if self.file_index >= len(self.file_paths):
            self.file_index = len(self.file_paths) - 1
        if len(self.file_paths) <= 0 or self.file_index >= len(self.file_paths):
            return None
        cur_path = self.file_paths[self.file_index]
        # self.ProcessImage(cur_path)
        return cur_path

    # 上一个文件
    def FilePrevious(self):
        # 文件索引减 1
        self.file_index -= 1
        if self.file_index < 0:
            self.file_index = 0
        if len(self.file_paths) <= 0 or self.file_index >= len(self.file_paths):
            return None
        # 当前路径
        cur_path = self.file_paths[self.file_index]
        # self.ProcessImage(cur_path)
        return cur_path
