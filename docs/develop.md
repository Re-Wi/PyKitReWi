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