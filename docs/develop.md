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

# 自动文档 MkDocs + mkdocstrings

```shell
pip install mkdocs mkdocstrings mkdocs-material
```

## 初始化 MkDocs 配置

```shell
mkdocs new PyKitReWi
```

## 构建文档

```shell
mkdocs build
```

## 运行本地服务器

```shell
mkdocs serve
```

# 自动文档  Sphinx + autodoc

```shell
pip install sphinx
```

## 初始化 Sphinx 配置： 在库的根目录下运行：

```shell
sphinx-quickstart
```

## 配置 autodoc： 在 conf.py 中添加 autodoc 扩展：

```python
extensions = ['sphinx.ext.autodoc']
```

生成文档： 在库代码中为你的函数、类、方法添加 docstring，然后在 Sphinx 的 .rst 文件中使用 autodoc 指令来自动提取这些
docstring 生成文档

```rst
.. automodule:: your_module
   :members:
```

## 构建文档： 使用以下命令生成 HTML 格式的文档：

```shell
make html
```

# 常见的格式是 Google 风格的 docstring 格式。

这种注释规范通常是用于 Python 中的文档字符串（docstring），它是为了详细说明函数、方法或类的参数、返回值和用法。常见的格式是
Google 风格的 docstring 格式。

1. **Args:** 列出了所有函数参数的名称、类型以及它们的作用。
2. **Returns:** 说明了函数的返回值的类型及其含义。
3. **Usage:** 通常用于提供一些用法示例，帮助开发者理解如何调用该函数。

## 风格

在 Python 中，有几种常见的文档字符串（docstring）风格，每种风格具有不同的格式和规范。以下是一些主要的 docstring 风格：

### 1. **Google 风格**

这种风格清晰、简洁，通常被很多 Python 项目使用，尤其是在 Google 的开源项目中。它以 **Args**、**Returns**、**Raises**
等关键词来组织文档。

**示例：**

```python
def connect_signal(class_type, signal_sender, signal_receiver):
    """
    Connects a signal sender to a signal receiver (slot function).

    Args:
        class_type (type): The class type to instantiate (class object).
        signal_sender (object): The object that sends the signal (should have a signal mechanism).
        signal_receiver (Callable): The function to connect as the signal receiver (slot function).

    Returns:
        object: The instantiated class object.

    Raises:
        ValueError: If the signal_sender is invalid.
    """
    pass
```

### 2. **NumPy/SciPy 风格**

NumPy 和 SciPy 的文档风格与 Google 风格类似，但它在参数描述部分的格式有所不同，特别是对可选参数和默认值的描述。

**示例：**

```python
def connect_signal(class_type, signal_sender, signal_receiver):
    """
    Connects a signal sender to a signal receiver (slot function).

    Parameters
    ----------
    class_type : type
        The class type to instantiate (class object).
    signal_sender : object
        The object that sends the signal (should have a signal mechanism).
    signal_receiver : Callable
        The function to connect as the signal receiver (slot function).

    Returns
    -------
    object
        The instantiated class object.

    Raises
    ------
    ValueError
        If the signal_sender is invalid.
    """
    pass
```

### 3. **reStructuredText（reST）风格**

reStructuredText 风格是 Python 文档工具（如 Sphinx）使用的默认风格。它通常用于生成文档，特别是用于 Python 项目的 API
文档。它使用 `:param`, `:type`, `:return` 等标记。

**示例：**

```python
def connect_signal(class_type, signal_sender, signal_receiver):
    """
    Connects a signal sender to a signal receiver (slot function).

    :param class_type: The class type to instantiate (class object).
    :type class_type: type
    :param signal_sender: The object that sends the signal (should have a signal mechanism).
    :type signal_sender: object
    :param signal_receiver: The function to connect as the signal receiver (slot function).
    :type signal_receiver: Callable
    :return: The instantiated class object.
    :rtype: object
    :raises ValueError: If the signal_sender is invalid.
    """
    pass
```

### 4. **Epytext 风格**

Epytext 是一种较旧的 Python docstring 风格，广泛用于早期的 Python 项目。它与 reStructuredText 相似，但稍微简化了标记格式。

**示例：**

```python
def connect_signal(class_type, signal_sender, signal_receiver):
    """
    Connects a signal sender to a signal receiver (slot function).

    @param class_type: The class type to instantiate (class object).
    @type class_type: type
    @param signal_sender: The object that sends the signal (should have a signal mechanism).
    @type signal_sender: object
    @param signal_receiver: The function to connect as the signal receiver (slot function).
    @type signal_receiver: Callable
    @return: The instantiated class object.
    @rtype: object
    @raise ValueError: If the signal_sender is invalid.
    """
    pass
```

### 5. **Plain Text 风格**

有些项目可能会选择最简洁的方式来编写 docstring，即不使用任何特定格式或标记，而仅仅提供普通的文本说明。这种风格通常是手动书写的，并且没有结构化的信息。

**示例：**

```python
def connect_signal(class_type, signal_sender, signal_receiver):
    """
    Connects a signal sender to a signal receiver.
    
    This function instantiates the class provided by `class_type` and connects 
    the `signal_sender` to the `signal_receiver`. It raises a ValueError if 
    the signal_sender is not valid.
    """
    pass
```

### 兼容性

关于不同风格之间的兼容性，实际上每种风格的文档字符串都是兼容的，因为它们都是以纯文本格式存储在 Python
文件中的。关键的不同在于如何解析这些字符串：

1. **自动化工具支持：**
    - **Google 风格**和**NumPy/SciPy 风格**都可以通过工具（如 **PyDoc**, **Sphinx**, **pdoc**）生成文档，支持自动化解析。
    - **reStructuredText 风格**通常用于 **Sphinx** 生成更复杂的 HTML 和 LaTeX 文档。
    - **Epytext 风格**主要用于早期的工具和框架，如 **Epytext**，虽然现在已不再广泛使用。
    - **Plain Text 风格**没有结构化的标记，因此无法与工具自动生成文档，但对开发者仍然清晰可读。

2. **文档工具兼容性：**
    - **Sphinx** 和 **PyDoc** 都能够解析 **reStructuredText** 和 **Google 风格**，并生成良好的文档。
    - **Sphinx** 可以通过 `napoleon` 扩展支持 **Google 风格** 和 **NumPy 风格**，因此它们在 Sphinx 中是兼容的。
    - 对于 **Epytext** 和 **Plain Text 风格**，虽然它们不如前两者在文档生成方面那么强大，但它们仍然可以作为常规文档说明被理解和使用。

### 总结

- **兼容性**：虽然不同的 docstring 风格之间有些差异，但它们都以纯文本形式存储，因此在基本的阅读和理解上是兼容的。不同风格的主要区别在于它们是否容易与自动化工具（如
  **Sphinx**, **PyDoc**）兼容。
- **选择合适的风格**：如果你的项目需要自动生成文档或与其他工具兼容，建议使用 **Google 风格** 或 **reStructuredText 风格**
  。如果只是为了可读性或简单说明，**Plain Text 风格** 也可以，但不支持自动化工具的文档生成。

## 各种参数格式的类型

除了 `Args:` 和 `Returns:`，还有其他几种常见的参数注释规范：

1. **Raises:** 用于列出函数可能引发的异常类型。
   ```text
   Raises:
       ValueError: If the input is invalid.
   ```

2. **Attributes:** 用于类的 docstring，列出类的属性。
   ```text
   Attributes:
       attribute_name (type): Description of the attribute.
   ```

3. **Example:** 用于提供具体的代码示例，通常位于 `Usage:` 部分，或者独立作为 `Example`。
   ```text
   Example:
       >>> my_function(1, 2)
       3
   ```

4. **Note:** 用于提供额外的备注信息，通常是补充说明。
   ```text
   Note:
       This method is only available in version 2.0 and above.
   ```

5. **Warning:** 用于提醒用户潜在的危险或副作用。
   ```text
   Warning:
       This function may alter global state.
   ```

6. **Todo:** 用于标记未来需要完成的任务。
   ```text
   Todo:
       Refactor this function for better performance.
   ```

## 示例

```python
def connect_signal(class_type, signal_sender, signal_receiver):
    """
    Connects a signal sender to a signal receiver (slot function).

    Args:
        class_type (type): The class type to instantiate (class object).
        signal_sender (object): The object that sends the signal (should have a signal mechanism).
        signal_receiver (Callable): The function to connect as the signal receiver (slot function).

    Returns:
        object: The instantiated class object.

    Usage:
        signal = connect_signal(MyClass, sender, receiver)
    """
    pass
```

[程序结构](./structure.md)