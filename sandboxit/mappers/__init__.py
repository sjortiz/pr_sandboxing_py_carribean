class Graph:

    config = {}

    @classmethod
    def remove_ignores(cls, data, _key=''):
        # This class reads from the config ignored section in the config.yaml
        # and excludes from the response any repo that has
        # it's name in that list

        data = data.get('data', {})

        if 'user' in data:
            data = data['user']

        elif 'organization' in data:
            data = data['organization']

        data = (
            data.get('repositories', {})
            .get('nodes', [])
        )

        repositories = [
            repo
            for repo in data
            if not repo.get('name') in cls.config.get('ignore', '')
        ]

        return repositories
