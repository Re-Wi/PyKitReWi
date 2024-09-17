# -*- coding: utf-8 -*-
"""修正自动生成代码中资源文件报错"""
import os
import re


def FixErrorLine(assets_folder: str, resources_folder: str):
    if not os.path.exists(assets_folder):
        print(f"The directory '{assets_folder}' does not exist.")
        return
    # 遍历 assets 文件夹中的所有文件
    for filename in os.listdir(assets_folder):
        # 检查文件是否以 _ui.py 结尾
        if filename.endswith('_ui.py'):
            # 构建文件的完整路径
            file_path = os.path.join(assets_folder, filename)

            # 打开文件以读取内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 使用正则表达式查找 import YYY_rc 行
            import_lines = re.findall(r'import (\w+)_rc', content)
            print(import_lines)

            for import_line in import_lines:
                # 检查文件中是否已经存在 'from assets import YYY_rc'
                if f'from {resources_folder} import {import_line}_rc' not in content:
                    # 如果不存在，则将 import YYY_rc 行改为 'from assets import YYY_rc'
                    modified_line = f'from {resources_folder} import {import_line}_rc'
                    content = content.replace(f'import {import_line}_rc', modified_line)
            # 写入修改后的内容回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
    print("Done! Modified import statements in XXX_ui.py files.")
