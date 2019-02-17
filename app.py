import os

import requests

from queries.prs import query_prs_from_user


Token = os.getenv('PR_SANDBOXING_TOKEN')


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

    to_kill = []
    to_create = []
    to_maintain = []

    for repo in unparsed_repos:

        _open = repo.get('open', {}).get('nodes', [])
        _merged = repo.get('merged', {}).get('nodes', [])
        _closed = repo.get('closed', {}).get('nodes', [])
