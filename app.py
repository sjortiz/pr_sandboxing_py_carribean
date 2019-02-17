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

    r = r.json().get('data', {}).get('user', {}).get('repositories', {})

    if r:

        unparsed_repos = r.get('nodes')

        repos = [
            {'name': repo['name'], 'open': repo['open']['prs']}
            for repo in unparsed_repos
            if repo['open']['prs']
        ]

        print(repos)
