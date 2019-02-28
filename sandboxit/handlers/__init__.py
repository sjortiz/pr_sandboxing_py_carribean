"""Module to transform plain data in objects with methods"""

# Built-in imports
import datetime


class Git:
    """Reshape and manage all the git related processes"""

    def __init__(self, data: list) -> None:
        """Receives the data and and fill the Git object"""
        self.__ssh_url = data.get('sshUrl')
        self.__prs = data.get('pullRequests', {}).get('nodes', [])
        self.__prs = Git.__re_structure_prs(self.__prs)
        self.__fetched = None

    @staticmethod
    def __re_structure_prs(prs: list) -> dict:
        """Group the prs by stage into a dictionary
        e.g:
        [
            {"id": 1, "state": "MERGED"}, ...,
            {"id": 90, "state": "OPEN"}, ...
        ]
        returns
        {
            'MERGED': [{"id": 1, "state": "MERGED"}, ...],
            'OPEN': [{"id": 90, "state": "OPEN"}, ...]
        }
        """
        __prs = {
            'MERGED': [],
            'OPEN': [],
            'CLOSED': [],
        }

        for pr in prs:
            __prs[pr.get('state')].append(pr)

        return __prs


    def clone(self):
        """Clone repo into local folder
        TODO:
            - Logic to clone
        """

        __open_prs = self.__prs.get('OPEN')

        if __open_prs:

            if not self.__fetched:

                print('Pulling repository')
                self.__fetched = datetime.datetime.now().time()


    def pull(self): ...
        """Updates the branch if there is any changes in the PR
        TODO:
            - Comparision with last commit id
            - Checkout and pull branch into new folder
        """



class Docker:
    def __init__(self, data: list):
        pass

    def pull(self): ...
