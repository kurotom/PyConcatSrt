# -*- coding: utf-8 -*-
"""
"""


from datetime import datetime


class ErrorData(object):

    id_file = 0

    def __init__(self):
        self.files = {}
        self.data = []

    def register(self, filename: str, error: list | str = None):
        if filename not in list(self.files.keys()):
            self.files[filename] = ErrorData.id_file
            ErrorData.id_file += 1
            self.data.append([error])
        else:
            if isinstance(error, list):
                self.data[self.files[filename]] = error
            else:
                self.data[self.files[filename]].append(error)

    def writeLog(self):
        date = datetime.now()
        msg = f"{date}\n\n"
        for k, v in self.files.items():
            lines = ", ".join(list(map(lambda x: str(x), self.data[v])))
            msg += 'File: "{0}", Error Lines: {1}\n'.format(k, lines)

        msg += '\n' + '=' * 30 + "\n"

        with open('Error_lines.log', 'w') as file:
            file.write(msg)

    def __str__(self):
        return f'files: {list(self.files.keys())}, line_errors: {self.data}'
