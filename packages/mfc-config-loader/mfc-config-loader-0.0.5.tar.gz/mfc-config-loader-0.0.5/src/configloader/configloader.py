from collections import namedtuple
import os
import re
import yaml


class ConfigLoader:
    def __init__(self, file_paths=None):
        self.file_paths = ['.config.yaml'] if file_paths is None else file_paths

    @classmethod
    def __read_file(cls, path: str) -> str:
        """
        Read the contents of a file.
        :param path: The path to the file.
        :return: The contents of the file.
        """
        with open(path, 'r', encoding='utf-8') as conf_data:
            return conf_data.read()

    @staticmethod
    def load_from_string(data=None, node=None):
        """
        Load configuration data from a string.
        :param data: A string representing the configuration data in YAML format.
        :param node: The key or path of the node in the configuration to load.
                     Defaults to None, which loads the entire configuration.
        :return: A named tuple representing the loaded configuration.
        """
        config_data = yaml.safe_load(data or '')

        def get_value(configs: dict, path: str):
            res_value = configs
            if path is not None:
                path_parts = path.split('.')
                for key in path_parts:
                    if '[' in key and ']' in key:
                        key, index = key[:-1].split('[')
                        index = int(index)
                        res_value = res_value.get(key)[index]
                    else:
                        res_value = res_value.get(key) if isinstance(res_value, dict) else None
            return res_value

        def parse_list(node):
            nodes_list = []
            for item in node:
                nodes_list.append(parse_dict_node(item))
            return nodes_list

        def parse_dict_node(node):
            regex_pattern = r'(?<!\$)\$\{([^}]*)}'
            ConfigurationsNode = namedtuple(typename='ConfigNode', field_names=node.keys())
            temp_config_data = {}
            for key, value in node.items():
                if isinstance(value, dict):
                    temp_config_data[key] = parse_dict_node(value)
                elif isinstance(value, list):
                    temp_config_data[key] = parse_list(value)
                else:
                    matches = re.findall(regex_pattern, str(value))
                    if matches:
                        for match in matches:
                            if ':' in match:
                                sub = os.environ.get(match.split(':')[1])
                            else:
                                sub = get_value(config_data, match)
                            var_pattern = re.compile(r"(?<!\$)\$\{" + match + "}")
                            value = var_pattern.sub(sub if sub is not None else f'${{{match}}}', str(value))
                    node[key] = value
                    temp_config_data[key] = value
            return ConfigurationsNode(**temp_config_data)

        if node is not None and isinstance(config_data[node], list):
            return parse_list(config_data[node])

        return parse_dict_node(config_data if node is None else config_data[node])

    def load(self, node=None):
        """
        Load configuration data from multiple files.
        :param file_paths: A list of file paths to load the configuration data from.
                           Defaults to an empty list if not provided.
        :param node: Optional node parameter to specify a specific node to load from the configuration data.
                     Defaults to None if not provided.
        :return: The loaded configuration data as a dictionary.
        """
        config_data_agg = "".join(self.__read_file(path) for path in (self.file_paths or []))
        return ConfigLoader.load_from_string(config_data_agg, node)
