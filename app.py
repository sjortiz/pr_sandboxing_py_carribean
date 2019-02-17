import os

import requests


Token = os.getenv('PR_SANDBOXING_TOKEN')


if __name__ == '__main__':
    r = requests.post(
        'https://api.github.com/graphql',
        json={
            'query': '''
                query {
                    user(login: "sjortiz") {
                        repositories(first: 100) {
                            nodes {
                                name
                                open: pullRequests(first: 100, states: OPEN) {
                                prs: nodes {
                                        number
                                    }
                                }
                            }
                        }
                    }
                }
            '''
        },
        headers={
            'Authorization': f'bearer {Token}'
        }
    )

    print(r.text)
