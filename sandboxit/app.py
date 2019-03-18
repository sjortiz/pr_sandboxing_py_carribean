# Built-in dependencies
import time
# Custom dependencies
from utils import Yaml, miscellaneous
from queries import Executor
from mappers import Graph
from handlers import Git
from handlers import Docker


class Storage:

    __instance = None
    instances = {}

    def __new__(cls, *args, **kwargs):

        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __getattr__(cls, attr):
        return cls[attr]


class Runner:

    __instance = None

    def __new__(cls, *args, **kwargs):

        if not cls.__instance:
            cls.__instance = object.__new__(cls)

        return cls.__instance

    def __init__(self, repositories_data):

        print('executed')

        try:
            self.__storage

        except AttributeError:
            self.__storage = Storage()

        self.repositories_data = repositories_data
        self.handler()

    def handler(self):

        for repo in self.repositories_data:

            name = repo.get('name')

            if name not in self.__storage.instances:

                git = Git(repo)
                docker = Docker(repo)

                self.__storage.instances[name] = {
                    'git': git,
                    'docker': docker,
                }

            else:

                self.__storage.instances[name]['git'].differ(repo)
                self.__storage.instances[name]['docker'].differ(repo)


if __name__ == '__main__':

    config = miscellaneous.fill_env_vars(
        Yaml.read_yaml('config.yaml'))
    Graph.config = config
    executor = Executor(config)

    while True:

        data = executor.retrieve_data()
        runner = Runner(repositories_data=Graph.remove_ignores(data))
        time.sleep(5)
