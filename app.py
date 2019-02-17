import subprocess
import time
from os import environ, makedirs, path

import requests

import git

from queries.prs import query_prs_from_user


Token = environ.get('PR_SANDBOXING_TOKEN')

__open = []
__killed = []


def kill_container(pr_name, branch, ssh_url):

    global __killed

    if not pr_name in __open:

        __killed.append(pr_name)
        return

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

        __killed.append(pr_name)
        __open.remove(pr_name)


def create_container(pr_name, branch, ssh_url):

    if not pr_name in __open:

        url = f'{pr_name}.docker'

        print(f'Spinning {pr_name}')

        folder_address = f'./pulls/{pr_name}'

        makedirs(folder_address, exist_ok=True)

        if not ssh_url:
            print('no ssh')
            return

        try:
            git.Repo.clone_from(
                ssh_url, folder_address, branch=branch)

        except Exception as e:

            print(f'ssh_url: {ssh_url}', f'folder address: {folder_address}', branch)

            print(
                f'This repo <<{ssh_url}>> could not be cloned.'
                'Trying to update'
            )

            git.Git(f'{folder_address}').pull('origin', branch)

        else:
            print(f'Repository {ssh_url}, clonned from branch {branch}')

        sp = subprocess.Popen(
            ['docker-compose', 'up', '--remove-orphans', '--detach'],
            stdout=subprocess.PIPE,
            cwd=folder_address,
            env={
                **environ,
                'web_address': url,
                'container_name': f'{pr_name}',
            },
        )

        print(url)

        __open.append(pr_name)


def iterate(name, pr_list, ssh_url, func):

    for pr in pr_list:

        compounded_name = f'{name}-{pr.get("number")}'
        func(compounded_name, pr.get('branch'), ssh_url)


def kill_containers(repo_name, prs, ssh_url):
    iterate(repo_name, prs, ssh_url, kill_container)


def create_containers(repo_name, prs, ssh_url):
    iterate(repo_name, prs, ssh_url, create_container)


def parse_pr_numbers(prs: list) -> list:
    return [
        {'number': pr.get('number'), 'branch': pr.get('branch')}
        for pr in prs
    ]


def split_data(repo: list) -> [list, list, list]:
    return (
        parse_pr_numbers(repo.get('open', {}).get('nodes', [])),
        parse_pr_numbers(repo.get('merged', {}).get('nodes', [])),
        parse_pr_numbers(repo.get('closed', {}).get('nodes', [])),
    )


def monitor():

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
        _ssh_url = repo.get('sshUrl', '')
        _open, _merged, _closed = split_data(repo)
        _finish_status = _merged + _closed

        create_containers(_name, _open, _ssh_url)
        kill_containers(_name, _finish_status, _ssh_url)



if __name__ == '__main__':

    while True:
        monitor()
        time.sleep(5)
