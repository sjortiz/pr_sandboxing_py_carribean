# built in imports
from os import environ, makedirs, scandir, listdir
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
                config[key] = environ.get(value[1:])

        return config

    @staticmethod
    def generate_folder(path: str, name: str) -> None:

        if not miscellaneous.find_file(path, name):
            makedirs(path+name)

    @staticmethod
    def find_file(path: str, name: str) -> Union[object, None]:

        with scandir(path) as it:

            for entry in it:

                if entry.name == name:
                    return entry
        return None

    @staticmethod
    def list_files_in_directory(path: str) -> list:
        return listdir(path)


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
