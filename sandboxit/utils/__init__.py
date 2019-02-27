import os

class Files:

    @staticmethod
    def read_file(file: str, location: str=''):

        if location:
            file = f'{location}/{file}'

        with open(file) as fi:
            return fi.read()
