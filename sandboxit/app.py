# Custom dependencies
from utils import Yaml, miscellaneous
from queries import executor
from mappers import Graph


class Runner:

    def __init__(self): ...

    def handler(): ...

    def create_env(): ...

    def destroy_env(): ...


if __name__ == '__main__':

    config = miscellaneous.fill_env_vars(Yaml.read_yaml('config.yaml'))
    data = executor(config).retrieve_data()
    Graph.config = config
    Graph.remove_ignores(data)
    Runner()
