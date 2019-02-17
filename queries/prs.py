def query_prs_from_user(user: str) -> str:

    return '''
        query {
            user(login: "%s") {
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
    ''' % user
