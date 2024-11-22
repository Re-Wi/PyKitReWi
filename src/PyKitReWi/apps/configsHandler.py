# -*- coding: UTF-8 -*-
"""
@Project    : PyKitReWi
@File       : configsHandler.py.py
@IDE        : PyCharm
@Author     : ReWi  # 替换为当前系统用户名（方便开发人员区分）
@Date       : 2024/11/23 1:52  # 日期和时间精确到秒
@License    : MIT
@Contact    : RejoiceWindow <RejoiceWindow@yeah.net>
@Description: 兼容三种常用配置文件，加载到命名空间做全局变量
@Version    : v0.0.0
@Dependencies: 
    - os
    - argparse
    - glob
    - pyyaml   （可选）
    - json     （可选）
    - tomli    （可选）
@Changelog  : 
    - v0.0.0 (2024/11/23 1:52): Initial version, implemented the core functionality.
    - v0.0.1 (2024/11/23 1:52)  # 记录文件版本更新的日志，例如修复的bug、增加的功能等
"""
import os
import argparse
import glob
from ..utils.constants import DEFAULT_CONFIG


def Dict2Namespace(namespace, config):
    """
    Recursively convert a dictionary to a namespace object.
    """
    if namespace is None:
        namespace = argparse.Namespace()
    for key, value in config.items():
        if isinstance(value, dict):
            new_value = Dict2Namespace(getattr(namespace, key, None), value)
        else:
            new_value = value
        setattr(namespace, key, new_value)

    return namespace


class ConfigsHandler:
    """
    A handler class for loading configuration files (YAML, JSON, TOML).
    Supports default config, auto-search, and imports.
    """
    file_dir = 'data/config/'  # Default directory
    namespace = argparse.Namespace()

    def __init__(self, file_path="", autoSearch=False):
        """
        Initialize the configuration handler, loading the config from the specified file path,
        or default directory, or by enabling auto search.

        :param file_path: Path to the config file (optional). If not provided, defaults to 'conf.yaml' in default directory.
        :param autoSearch: If True, enables searching the current directory for YAML files to load.
        """
        # Initialize with default config
        self.configs = Dict2Namespace(self.namespace, DEFAULT_CONFIG)

        # Priority check for file_path, then default directory or auto-search
        if file_path and os.path.exists(file_path):
            # If file_path is provided and the file exists, load the specified file
            self._load_config_file(file_path)
        else:
            # If file_path is not provided, check the default directory for conf.* file
            config_files = glob.glob(os.path.join(self.file_dir, "conf.*"))

            if config_files:
                # If conf.* exists in the default directory, load the first matching file
                self._load_config_file(config_files[0])

        # If autoSearch is enabled, search the current directory for any config files
        if autoSearch:
            self._search_and_load_files(os.getcwd())

    def _search_and_load_files(self, search_dir):
        """
        Search for all configuration files in the specified directory and load them.
        :param search_dir: Directory to search for configuration files (YAML, JSON, TOML).
        """
        config_files = [f for f in os.listdir(search_dir) if f.endswith(('.yaml', '.json', '.toml'))]

        if not config_files:
            print(f"No configuration files found in {search_dir}.")
            return

        for config_file in config_files:
            config_path = os.path.join(search_dir, config_file)
            self._load_config_file(config_path)

    def _load_config_file(self, file_path):
        """
        Load a configuration file (YAML, JSON, or TOML) and update the configuration.
        :param file_path: Path to the configuration file.
        """
        file_extension = os.path.splitext(file_path)[1].lower()

        try:
            if file_extension == '.yaml':
                self._load_yaml_file(file_path)
            elif file_extension == '.json':
                self._load_json_file(file_path)
            elif file_extension == '.toml':
                self._load_toml_file(file_path)
            else:
                print(f"Unsupported config file type: {file_extension}")
        except Exception as err:
            print(f"Error loading {file_path}: {err}")

    def _load_yaml_file(self, file_path):
        """
        Load a YAML file and update the configuration.
        :param file_path: Path to the YAML file.
        """
        import yaml
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                # 更新现有的配置，避免覆盖
                updated_config = {**vars(self.configs), **config}

                # 递归将字典转为 Namespace 对象
                self.configs = Dict2Namespace(self.namespace, updated_config)

                # 如果配置文件中有 'import' 字段，处理递归加载
                self._load_imports(config, os.path.dirname(file_path))
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except yaml.YAMLError as e:
            print(f"Error: Failed to decode yaml from {file_path}: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred while loading {file_path}: {e}")

    def _load_json_file(self, file_path):
        """
        Load a JSON file and update the configuration.
        :param file_path: Path to the JSON file.
        """
        import json
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

                # 更新现有的配置，避免覆盖
                updated_config = {**vars(self.configs), **config}

                # 递归将字典转为 Namespace 对象
                self.configs = Dict2Namespace(self.namespace, updated_config)

                # 如果配置文件中有 'import' 字段，处理递归加载
                self._load_imports(config, os.path.dirname(file_path))

        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from {file_path}: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred while loading {file_path}: {e}")

    def _load_toml_file(self, file_path):
        """
        Load a TOML file and update the configuration.
        :param file_path: Path to the TOML file.
        """
        import tomli

        try:
            # 以二进制模式打开文件
            with open(file_path, 'rb') as f:  # 注意这里的 'rb'
                config = tomli.load(f)  # 使用 tomli 解析 TOML 文件

                # 更新配置，避免覆盖现有配置
                updated_config = {**vars(self.configs), **config}

                # 使用 Dict2Namespace 将字典转换为命名空间对象
                self.configs = Dict2Namespace(self.namespace, updated_config)
                # 检查 TOML 配置中的 'import' 字段并递归加载
                self._load_imports(config, os.path.dirname(file_path))

        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except tomli.TOMLDecodeError as e:
            print(f"Error: Failed to decode TOML from {file_path}: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred while loading {file_path}: {e}")

    def _load_imports(self, config, base_dir):
        """
        Check and load configuration files specified in the 'import' field within a config.
        :param config: The loaded configuration.
        :param base_dir: The base directory where the config file was located.
        """
        if 'import' in config:
            for import_file in config['import']:
                import_path = os.path.join(base_dir, import_file)
                if os.path.exists(import_path):
                    self._load_config_file(import_path)
                else:
                    print(f"Warning: Import file '{import_file}' not found. It will be skipped.")

    def add_config_file(self, file_path):
        """
        Dynamically add a new configuration file to the configuration.
        :param file_path: Path to the configuration file to be added.
        :return: True if the file was successfully added, False otherwise.
        """
        if os.path.exists(file_path):
            self._load_config_file(file_path)
            return True
        else:
            print(f"Warning: The file {file_path} does not exist.")
            return False

    def __getattr__(self, name):
        """
        Allows direct access to configuration attributes, specific to this instance.
        For example, `config_handler.someConfigKey` will work directly if `someConfigKey` is in the config.
        This does not affect other instances of the class.

        :param name: The attribute name to access.
        :return: The value of the attribute if it exists in the config.
        :raises AttributeError: If the attribute is not found.
        """
        if hasattr(self.configs, name):
            return getattr(self.configs, name)
        elif name in vars(self.configs):
            return getattr(self.configs, name)
        raise AttributeError(f"'ConfigsHandler' object has no attribute '{name}'")
