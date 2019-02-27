from queries import Queries

params = {
    'entity': 'user',
    'entity_login': 'sjortiz',
    'limit': 100,
}

print(Queries(**params).prs())
