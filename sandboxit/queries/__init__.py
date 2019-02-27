# Built-in dependencies
from typing import Union

# Third-party dependencies
import requests

# Custom imports
from utils import Yaml, miscellaneous
from utils import Files


class Queries(object):

    __prs_query = Files.read_file('prs.graphql', location='./queries/')

    def __init__(
            self, entity: str, entity_login: str,
            limit: int = 100, **kwargs) -> None:

        self.__params = {
            'entity': entity,
            'entity_login': entity_login,
            'limit': limit,
        }

    def prs(self):
        return Queries.__prs_query.format(**self.__params)


class executor(Queries):

    def __init__(self):

        self.__config = miscellaneous.fill_env_vars(
            Yaml.read_yaml('config.yaml'))

        super().__init__(**self.__config['general'])

        config_api = self.__config.get('api', {})

        self.__api_url = config_api.get('url', '')
        self.__api_authorization = config_api.get('authorization', '')
        self.__api_token = config_api.get('token', '')
        self.__query = self.prs()

    def retrieve_data(self) -> Union[dict, None]:

        r = requests.post(
            self.__api_url,
            json={
                'query': self.__query
            },
            headers={
                'Authorization': (
                    f'{self.__api_authorization } '
                    f'{self.__api_token}')
            }
        )

        return r.json()
