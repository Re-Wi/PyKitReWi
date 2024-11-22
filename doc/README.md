# 如何在 PyCharm 中使用文件头模板

1. 配置 PyCharm 文件模板：

- 打开 PyCharm。
- 进入 File > Settings（Windows/Linux）或 PyCharm > Preferences（macOS）。
- 在设置窗口中，导航到 Editor > File and Code Templates。
- 在右侧窗口中，选择 Python Script 或者 Includes，然后在模板编辑器中添加或修改模板内容。

```python
# -*- coding: UTF-8 -*-
"""
@Project    : ${PROJECT_NAME}
@File       : ${NAME}.py
@IDE        : ${PRODUCT_NAME}
@Author     : ${USER}  # 替换为当前系统用户名（方便开发人员区分）
@Date       : ${DATE} ${TIME}  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description: ${DESCRIPTION}  # 这里可以填写简短的文件功能描述
@Version    : v0.0.0
@Dependencies: 
    - python3
@Changelog  : 
    - v0.0.0 (${DATE} ${TIME}): Initial version, implemented the core functionality.
    - v0.0.1 (${DATE} ${TIME})  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""
```

# pytest之命名规则和运行方式

1. 默认规则

```text
1. 模块名必须以test_开头或以_test结尾（如，test_login.py）

2. 测试类必须以Test开头，并且不能有init方法（如，class TestLogin:）

3. 测试方法必须以test开头（如，def test_01()或test02()）
```

# 程序自测

## 编译库

```shell
py -m build --wheel
```

## 库的安装

```shell
# 卸载旧版本
pip uninstall PyKitReWi -y
# 安装才编译的版本 
pip install .\dist\PyKitReWi + <Tab 键>
```

## 库的使用

1. 进入 tests 文件夹
2. 新建 test_* 文件自测

[程序结构](./structure.md)