"""Module to transform plain data in objects with methods"""

# Custom dependencies
from utils import miscellaneous


class Git:
    """Reshape and manage all the git related processes"""

    def __init__(self, data: dict) -> None:
        """Receives the data and and fill the Git object"""
        self.__repo_name = data.get('name', '')
        self.__ssh_url = data.get('sshUrl')
        self.__prs = data.get('pullRequests', {}).get('nodes', [])
        self.__prs = Git.__re_structure_prs(self.__prs)
        self.__folder_generate = False

        if 'OPEN' in self.__prs:
            self.__generate_main_folder()

    def differ(self, data: dict) -> None:
        ...

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
        _prs = {
            'MERGED': [],
            'OPEN': [],
            'CLOSED': [],
        }

        for pr in prs:
            _prs[pr.get('state')].append(Pr(pr))

        return _prs

    def __generate_main_folder(self) -> None:

        miscellaneous.generate_folder(
            f'./repositories/', self.__repo_name)

        self.__folder_generate = True


class Pr:

    def __init__(self, pr: dict, repo_name: str = None):

        self.__repo_name = repo_name
        self.__branch = pr['branch']
        self.__number = pr['number']
        self.__state = pr['state']
        self.__commits = (
            pr['commits']
            .get('nodes', [{}])[0]
            .get('commit', {})
            .get('id')
        )
        self.__cloned = False

    def clone(self) -> None:
        """Clone repo into local folder
        TODO:
            - Logic to clone
        """
        if not self.__cloned:

            miscellaneous.generate_folder(
                f'./repositories/{self.__repo_name}/', self.__number)

            self.__cloned = True

    def pull(self) -> None:
        """Updates the branch if there is any changes in the PR
            TODO:
                - Comparision with last commit id
                - Checkout and pull branch into new folder
        """
        ...


class Docker:
    def __init__(self, data: list) -> None:
        pass

    def differ(self, data: dict) -> None:
        ...

    def pull(self) -> None: ...
