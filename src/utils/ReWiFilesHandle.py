#以下是用Python实现读取文件夹下所有文件，并按文件名排序，再按变量重命名的代码
import os

directory = "./imgs2/" # 文件夹路径
files = os.listdir(directory) # 获取文件列表
files.sort() # 排序文件列表

# 遍历所有文件
for i, file_name in enumerate(files):
    full_path = os.path.join(directory, file_name) # 获取完整路径
    new_name = f"OSD_{i}.jpeg" # 新文件名，例如：file_1.txt、file_2.txt、file_3.txt...
    os.rename(full_path, os.path.join(directory, new_name)) # 重命名文件