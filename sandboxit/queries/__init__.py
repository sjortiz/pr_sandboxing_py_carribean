# Built-in dependencies
from typing import Union

# Third-party dependencies
import requests

# Custom imports
from utils import Files


class Queries(object):

    def __init__(
            self, entity: str, entity_login: str,
            limit: int = 100, **kwargs) -> None:

        self.__params = {
            'entity': entity,
            'entity_login': entity_login,
            'limit': limit,
        }

        self.pr_query = Queries.construct_query(
            Queries.get_query('prs.graphql', location='./queries/'),
            **self.__params)

    @staticmethod
    def construct_query(query: str, **kwargs: dict) -> str:

        limit = {
            'repository': 10,
            'pr': 10,
        }

        _kwargs_limit = kwargs.get('limit')

        if _kwargs_limit:

            if isinstance(_kwargs_limit, dict):
                limit = _kwargs_limit

            elif isinstance(_kwargs_limit, int):

                limit['repository'] = _kwargs_limit
                limit['pr'] = _kwargs_limit

        kwargs.update(limit)

        return query.format(**kwargs)

    @staticmethod
    def get_query(query: str, location: str = '') -> str:
        return Files.read_file(query, location=location)


class executor(Queries):

    def __init__(self, config):

        self.__config = config

        super().__init__(**self.__config['general'])

        config_api = self.__config.get('api', {})

        self.__api_url = config_api.get('url', '')
        self.__api_authorization = config_api.get('authorization', '')
        self.__api_token = config_api.get('token', '')

    def retrieve_data(self) -> Union[dict, None]:

        r = requests.post(
            self.__api_url,
            json={
                'query': self.pr_query
            },
            headers={
                'Authorization': (
                    f'{self.__api_authorization } '
                    f'{self.__api_token}')
            }
        )

        return r.json()
