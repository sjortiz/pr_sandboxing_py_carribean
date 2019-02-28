# Built-in dependencies
import time
from dataclasses import dataclass
# Custom dependencies
from utils import Yaml, miscellaneous
from queries import executor
from mappers import Graph
from handlers import Git
from handlers import Docker


@dataclass
class Storage:
    instances = dict()


class Runner:

    def __init__(self, repositories_data):

        self.__storage = Storage()
        self.repositories_data = repositories_data
        self.handler()

    def handler(self):

        for repo in self.repositories_data:

            name = repo.get('name')

            if name not in self.__storage.instances:
                self.__storage.instances[name] = {
                    'git': Git(repo),
                    'docker': Docker(repo),
                }

    def iterate(self):

        for repo in self.__storage.instances:

            repo = self.__storage.instances[repo]
            repo['git'].pull()
            repo['docker'].pull()


if __name__ == '__main__':

    config = miscellaneous.fill_env_vars(Yaml.read_yaml('config.yaml'))
    data = executor(config).retrieve_data()

    Graph.config = config
    runner = Runner(Graph.remove_ignores(data))

    while True:
        runner.iterate()
        time.sleep(5)
        print('\n\n')
