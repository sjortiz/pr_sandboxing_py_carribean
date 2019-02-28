import datetime


class Git:

    def __init__(self, data: list) -> None:

        self.__ssh_url = data.get('sshUrl')
        self.__prs = data.get('pullRequests', {}).get('nodes', [])
        self.__prs = Git.__re_structure_prs(self.__prs)
        self.__fetched = None

    @staticmethod
    def __re_structure_prs(prs: list) -> dict:

        __prs = {}

        for pr in prs:

            state = pr.get('state')

            if state in __prs:
                __prs[state].append(pr)

            else:
                __prs[state] = [pr]

        return __prs

    def pull(self):

        if self.__prs.get('OPEN'):

            if not self.__fetched:

                print('Pulling repository')
                self.__fetched = datetime.datetime.now().time()

            else:
                print('Pulling updates if any')


class Docker:
    def __init__(self, data: list):
        pass

    def pull(self): ...
