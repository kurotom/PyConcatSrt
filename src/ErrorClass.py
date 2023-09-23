# -*- coding: utf-8 -*-
"""
"""


class ErrorData(object):

    id_file = 0

    def __init__(self):
        self.files = {}
        self.data = []

    def register(self, filename, error):
        if filename not in list(self.files.keys()):
            self.files[filename] = ErrorData.id_file
            ErrorData.id_file += 1
            self.data.append([error])
        else:
            self.data[self.files[filename]].append(error)

    def __str__(self):
        return f'files: {list(self.files.keys())[0]}, line_errors: {self.data}'
