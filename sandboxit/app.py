# custom dependencies
from utils import Yaml, miscellaneous
from queries import Queries

config = miscellaneous.fill_env_vars(Yaml.read_yaml('config.yaml'))

Queries(**config['general']).prs()
