# built in imports
import os
from typing import Union
# third party imports
from yaml import safe_load, YAMLError


class miscellaneous:

    @staticmethod
    def fill_env_vars(config: dict) -> dict:

        for key, value in config.items():

            if isinstance(value, dict):
                config[key] = miscellaneous.fill_env_vars(value)

            elif isinstance(value, str) and value.startswith('$'):
                config[key] = os.environ.get(value[1:])

        return config


class Files:

    @staticmethod
    def read_file(file: str, location: str = '') -> Union[str, None]:
        if location:
            file = f'{location}/{file}'

        with open(file) as fi:
            return fi.read()


class Yaml:

    @staticmethod
    def read_yaml(file: str, location: str = '') -> dict:

        yaml_file = {}

        try:
            yaml_file = safe_load(Files.read_file(file, location))

        except YAMLError as e:
            print(e)

        return yaml_file
