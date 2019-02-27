from utils import Files


class Queries:

    __prs_query = Files.read_file('prs.graphql', location='./queries/')

    def __init__(self, entity, entity_login, limit):
        self.__params = {
            'entity': entity,
            'entity_login': entity_login,
            'limit': limit,
        }

    def prs(self):
        return Queries.__prs_query.format(**self.__params)
