from utils import Files


class Queries:

    __prs_query = Files.read_file('prs.graphql', location='./queries/')

    def __init__(
            self, entity: str, entity_login: str, limit: int = 100) -> None:

        self.__params = {
            'entity': entity,
            'entity_login': entity_login,
            'limit': limit,
        }

    def prs(self):
        return Queries.__prs_query.format(**self.__params)
