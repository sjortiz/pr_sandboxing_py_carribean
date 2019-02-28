class Graph:

    config = {}

    @classmethod
    def remove_ignores(cls, data, _key=''):
        # This class reads from the config ignored section in the config.yaml
        # and excludes from the response any repo that has
        # it's name in that list

        _tmp_dict = {}

        if isinstance(data, dict):

            if 'name' in data and data['name'] in cls.config.get('ignore', ''):
                return {}

            for key, value in data.items():
                _tmp_dict[key] = Graph.remove_ignores(value)

        elif isinstance(data, list):

            filtered = []

            for item in data:

                compute = Graph.remove_ignores(item)

                if compute:
                    filtered.append(compute)

            return filtered

        else:
            return data

        return _tmp_dict
