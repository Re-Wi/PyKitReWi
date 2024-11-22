# -*- coding: UTF-8 -*-
"""
@Project    : PyKitReWi
@File       : constants.py.py
@IDE        : PyCharm
@Author     : ReWi  # 替换为当前系统用户名（方便开发人员区分）
@Date       : 2024/11/22 23:09  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description: 专门存放常量。然后，在其他模块中导入它。
@Version    : v0.0.0
@Dependencies: 
    - python3
@Changelog  : 
    - v0.0.0 (2024/11/22 23:09): Initial version, implemented the core functionality.
    - v0.0.1 (2024/11/22 23:09)  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""
DEFAULT_CONFIG = {
    # APP相关配置
    "version": 'VMAJOR.MINOR.PATCH',
    "appname": 'ApplicationByReWi',
    # 常量
    "workDir": './',
    "datasRecorderTime": 1000,
    # 动态插件保存目录
    "pluginDir": 'plugins/',
    # 默认组件
    "moduleDir": 'windowUI/',
    # 其他配置文件所在文档
    "configDir": 'data/config/',
    "import": [],
}
