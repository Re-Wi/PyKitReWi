# -*- coding: UTF-8 -*-
"""
@Project    : PyKitReWi
@File       : developHelper.py
@IDE        : PyCharm
@Author     : ReWi  # 替换为当前系统用户名（方便开发人员区分）
@Date       : 2024/11/22 18:22  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description: 开发时需要自动执行的,如修正代码,可以 import 该文件进行
@Version    : v0.0.0
@Dependencies:
    - os
    - re
@Changelog  : 
    - v0.0.0 (2024/11/22 18:22): Initial version, implemented the core functionality.
    - v0.0.1 (2024/11/22 18:22)  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""
import os
import re


def ResourcesCodeFix(assets_folder: str = './', resources_folder: str = 'resources'):
    """
    Adjusts resource imports in generated code based on the development mode. If in development mode,
    fixes the import statements in generated Python files within the assets folder to avoid import errors.

    Args:
        assets_folder (str): Path to the assets folder containing the generated files. Defaults to './'.
        resources_folder (str): Path to the resources folder where fixed import targets are located. Defaults to 'resources'.

    Environment Variables:
        - APP_MODE: Determines whether the script operates in "DEBUG" mode (development). Defaults to "RELEASE" (non-development).

    Raises:
        ImportError: If required modules for fixing imports are missing, the function raises ImportError.
    """

    # Retrieve mode setting from environment variable and determine if development actions are needed.
    app_mode = os.getenv('APP_MODE', 'RELEASE').upper()
    if "DEBUG" not in app_mode:
        print("Skipping resource code fix: not in development mode.")
        return

    print("Development mode enabled. Proceeding with resource code fix.")

    # Check if assets folder exists, otherwise exit.
    if not os.path.exists(assets_folder):
        print(f"Assets directory '{assets_folder}' does not exist.")
        return

    # Process each file in the assets folder with '_ui.py' suffix for import adjustments.
    for filename in os.listdir(assets_folder):
        if filename.endswith('_ui.py'):
            file_path = os.path.join(assets_folder, filename)

            # Read the file's content to identify imports requiring adjustment.
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Use regex to find `import XYZ_rc` lines and adjust to `from resources_folder import XYZ_rc`.
            import_lines = re.findall(r'import (\w+)_rc', content)
            for import_line in import_lines:
                target_import = f'from {resources_folder} import {import_line}_rc'
                if target_import not in content:
                    content = content.replace(f'import {import_line}_rc', target_import)

            # Write back modified content.
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

    print("Resource code fix completed: modified import statements in *_ui.py files.")
