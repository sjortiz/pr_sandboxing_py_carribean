"""Module to transform plain data in objects with methods"""
# Built-in dependencies
import os
# Third-party dependencies
import sh
# Custom dependencies
from utils import miscellaneous


class Git:
    """Reshape and manage all the git related processes"""

    def __init__(self, data: dict) -> None:
        """Receives the data and and fill the Git object"""
        self.__repo_name = data.get('name', '')
        self.__ssh_url = data.get('sshUrl')
        self.__prs = data.get('pullRequests', {}).get('nodes', [])
        self.__prs = self.__re_structure_prs()
        self.__folder_generate = False
        self.__generate_main_folder()

        if 'OPEN' in self.__prs:

            for pr in self.__prs.get('OPEN', []):
                pr.clone()

    def differ(self, data: dict) -> None:
        # TODO: Logic to detect and update differences
        ...

    def __re_structure_prs(self) -> dict:
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

        for pr in self.__prs:

            # TODO: Logic to turn down
            _prs[pr.get('state')].append(Pr(
                pr, self.__repo_name, self.__ssh_url
            ))

        return _prs

    def __generate_main_folder(self) -> None:

        miscellaneous.generate_folder(
            f'./repositories/', self.__repo_name)

        self.__folder_generate = True


class Pr:

    def __init__(self, pr: dict,
                 repo_name: str, ssh_url: str) -> None:

        self.__repo_name = repo_name
        self.__ssh_url = ssh_url
        self.__branch = pr['branch']
        self.__number = str(pr['number'])
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
        and checkouts to the branch
        """

        if not self.__cloned:

            path = (f'./repositories/{self.__repo_name}',
                    self.__number)

            miscellaneous.generate_folder(*path)

            path = os.path.join(*path)

            git = sh.git.bake(_cwd=path)

            if miscellaneous.is_directory_empty(path):

                git = sh.git.bake(_cwd=path)
                git.clone(self.__ssh_url, '.')
                git.checkout(self.__branch)

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
        # TODO: Logic to detect and update differences
        ...

    def pull(self) -> None: ...
