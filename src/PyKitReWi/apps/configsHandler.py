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

    This function traverses the given dictionary and recursively converts
    it into an argparse.Namespace object, allowing access to configuration
    values via dot notation (e.g., `namespace.key`).

    Args:
        namespace (argparse.Namespace): The namespace object to update (if None, a new Namespace is created).
        config (dict): The dictionary containing configuration values.

    Returns:
        argparse.Namespace: The updated namespace with values from the dictionary.
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
    A handler class for loading and managing configuration files (YAML, JSON, TOML).

    Supports loading a default configuration, searching for configuration
    files in specified directories, and handling recursive imports from
    configuration files.

    Attributes:
        file_dir (str): The default directory for configuration files.
        namespace (argparse.Namespace): The namespace to hold the configuration values.
    """
    file_dir = 'data/config/'  # Default directory for configuration files
    namespace = argparse.Namespace()

    def __init__(self, file_path="", autoSearch=False):
        """
        Initializes the configuration handler and loads configurations
        from the specified file or directory.

        Args:
            file_path (str, optional): The path to a specific configuration file.
                If not provided, the default directory or auto-search is used.
            autoSearch (bool, optional): If True, enables searching the current
                directory for configuration files. Defaults to False.
        """
        # Initialize with the default configuration
        self.configs = Dict2Namespace(self.namespace, DEFAULT_CONFIG)

        # Priority check for file_path, then default directory or auto-search
        if file_path and os.path.exists(file_path):
            self._load_config_file(file_path)
        else:
            config_files = glob.glob(os.path.join(self.file_dir, "conf.*"))
            if config_files:
                self._load_config_file(config_files[0])

        if autoSearch:
            self._search_and_load_files(os.getcwd())

    def _search_and_load_files(self, search_dir):
        """
        Search for all configuration files in the specified directory and load them.

        Args:
            search_dir (str): The directory to search for configuration files (YAML, JSON, TOML).
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
        Load a configuration file (YAML, JSON, or TOML) and update the current configuration.

        Args:
            file_path (str): The path to the configuration file.
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

        Args:
            file_path (str): The path to the YAML configuration file.
        """
        import yaml
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                updated_config = {**vars(self.configs), **config}

                self.configs = Dict2Namespace(self.namespace, updated_config)
                self._load_imports(config, os.path.dirname(file_path))
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except yaml.YAMLError as e:
            print(f"Error: Failed to decode YAML from {file_path}: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred while loading {file_path}: {e}")

    def _load_json_file(self, file_path):
        """
        Load a JSON file and update the configuration.

        Args:
            file_path (str): The path to the JSON configuration file.
        """
        import json
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                updated_config = {**vars(self.configs), **config}

                self.configs = Dict2Namespace(self.namespace, updated_config)
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

        Args:
            file_path (str): The path to the TOML configuration file.
        """
        import tomli

        try:
            with open(file_path, 'rb') as f:
                config = tomli.load(f)
                updated_config = {**vars(self.configs), **config}

                self.configs = Dict2Namespace(self.namespace, updated_config)
                self._load_imports(config, os.path.dirname(file_path))
        except FileNotFoundError:
            print(f"Error: The file {file_path} does not exist.")
        except tomli.TOMLDecodeError as e:
            print(f"Error: Failed to decode TOML from {file_path}: {e}")
        except Exception as e:
            print(f"Error: An unexpected error occurred while loading {file_path}: {e}")

    def _load_imports(self, config, base_dir):
        """
        Check and recursively load configuration files specified in the 'import' field.

        Args:
            config (dict): The loaded configuration dictionary.
            base_dir (str): The directory where the configuration file is located.
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
        Dynamically add a new configuration file to the current configuration.

        Args:
            file_path (str): The path to the configuration file to be added.

        Returns:
            bool: True if the file was successfully added, False otherwise.
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

        Args:
            name (str): The attribute name to access.

        Returns:
            The value of the attribute if it exists in the configuration.

        Raises:
            AttributeError: If the attribute is not found in the configuration.
        """
        if hasattr(self.configs, name):
            return getattr(self.configs, name)
        elif name in vars(self.configs):
            return getattr(self.configs, name)
        raise AttributeError(f"'ConfigsHandler' object has no attribute '{name}'")
