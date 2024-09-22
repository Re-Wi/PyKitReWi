# PyKitReWi

![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")

A sample project that exists as an aid to the [Python Packaging User
Guide][packaging guide]'s [Tutorial on Packaging and Distributing
Projects][distribution tutorial].

This project does not aim to cover best practices for Python project
development as a whole. For example, it does not provide guidance or tool
recommendations for version control, documentation, or testing.

[The source for this project is available here][src].

Most of the configuration for a Python project is done in the `setup.py` file,
an example of which is included in this project. You should edit this file
accordingly to adapt this sample project to your needs.

----

This is the README file for the project.

The file should use UTF-8 encoding and can be written using
[reStructuredText][rst] or [markdown][md use] with the appropriate [key set][md
use]. It will be used to generate the project webpage on PyPI and will be
displayed as the project homepage on common code-hosting services, and should be
written for that purpose.

Typical contents for this file would include an overview of the project, basic
usage examples, etc. Generally, including the project changelog in here is not a
good idea, although a simple “What's New” section for the most recent version
may be appropriate.

[packaging guide]: https://packaging.python.org

[distribution tutorial]: https://packaging.python.org/tutorials/packaging-projects/

[src]: https://github.com/Re-Wi/PyKitReWi

[rst]: http://docutils.sourceforge.net/rst.html

[md]: https://tools.ietf.org/html/rfc7764#section-3.5 "CommonMark variant"

[md use]: https://packaging.python.org/specifications/core-metadata/#description-content-type-optional

# Packaging your project

- https://packaging.python.org/en/latest/guides/section-build-and-publish/

Before you can build wheels and sdists for your project, you’ll need to install the build package:

```shell
py -m pip install build
```

Source distributions
Minimally, you should create a Source Distribution:

```shell
py -m build --sdist
```

# Wheels

## Pure Python Wheels

Pure Python Wheels contain no compiled extensions, and therefore only require a single Python wheel.

To build the wheel:

```shell
py -m build --wheel
```

## Platform Wheels

Platform Wheels are wheels that are specific to a certain platform like Linux, macOS, or Windows, usually due to
containing compiled extensions.

```shell
py -m build --wheel
```

# 上传

- https://zhuanlan.zhihu.com/p/682004873

## 上传到TestPyPI

```shell
py -m twine upload --repository testpypi dist/*
```

## 上传到PyPI

```shell
py -m twine upload dist/*
```
