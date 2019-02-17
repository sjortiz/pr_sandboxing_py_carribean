import os
import subprocess

import requests

from queries.prs import query_prs_from_user


Token = os.getenv('PR_SANDBOXING_TOKEN')

__open = []
__killed = []


def kill_container(pr_name):

    if not pr_name in __killed:

        print(f'Attempting to kill pr {pr_name}')

        folder_address = f'pulls/{pr_name}'

        if path.exists(folder_address):

            print('PR Found!')

            print('killing')

            sp = subprocess.Popen(
                [
                    'docker-compose',
                    'down', '--remove-orphans'
                ],
                stdout=subprocess.PIPE,
                cwd=folder_address,
            )

        __killed = pr_name


def create_container(pr_name):

    if not pr_name in __open:
        print(pr_name, 'creating')


def iterate(name, pr_list, func):

    for pr in pr_list:

        compounded_name = f'{pr}-{name}'
        func(compounded_name)


def kill_containers(repo_name, prs):
    iterate(repo_name, prs, kill_container)


def create_containers(repo_name, prs):
    iterate(repo_name, prs, create_container)


def parse_pr_numbers(prs: list) -> list:
    return [
        pr.get('number')
        for pr in prs
    ]


def split_data(repo: list) -> [list, list, list]:
    return (
        parse_pr_numbers(repo.get('open', {}).get('nodes', [])),
        parse_pr_numbers(repo.get('merged', {}).get('nodes', [])),
        parse_pr_numbers(repo.get('closed', {}).get('nodes', [])),
    )


if __name__ == '__main__':

    repos = []
    open_prs = []
    query_prs_from_sjoritz = query_prs_from_user('sjortiz')

    r = requests.post(
        'https://api.github.com/graphql',
        json={'query': query_prs_from_sjoritz},
        headers={'Authorization': f'bearer {Token}'}
    )

    if r.json().get('errors') or not r.ok:

        print(r.text)
        exit(r.status_code)

    info = r.json().get('data', {}).get('user', {}).get('repositories', {})

    if not info:
        print('No repositories')

    unparsed_repos = info.get('nodes')

    for repo in unparsed_repos:

        _name = repo.get('name', '')
        _open, _merged, _closed = split_data(repo)
        _finish_status = _merged + _closed

        create_containers(_name, _open)
        kill_containers(_name, _finish_status)
