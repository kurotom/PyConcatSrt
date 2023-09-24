# -*- coding: utf-8 -*-
"""
Class that is responsible for storing and recording all format errors of the
srt file(s).
"""


from datetime import datetime
import os


class ErrorData(object):

    id_file = 0

    def __init__(self):
        self.files = {}
        self.data = []
        self.line_error = []
        self.total_errors = 0
        self.file_error_log = 'Error_lines.log'

    def getDataError(self, name) -> int:
        if name not in list(self.files.keys()):
            self.files[name] = ErrorData.id_file
            self.data.append([])
            self.line_error.append([])
            ErrorData.id_file += 1
            return self.files[name]
        else:
            return self.files[name]

    def registerIndex(self, filename: str, error: list | int = None) -> bool:
        id_error_list = self.getDataError(filename)
        if error is not None:
            if isinstance(error, list):
                self.data[id_error_list] += error
                self.total_errors += 1
                return True
            elif isinstance(error, int):
                self.data[id_error_list].append(error)
                self.total_errors += 1
                return True
            else:
                return False

    def registerLine(self, filename: str, error: list | int = None) -> bool:
        id_list = self.getDataError(filename)
        if error is not None:
            if isinstance(error, list):
                self.line_error[id_list] += error
                self.total_errors += 1
                return True
            elif isinstance(error, int):
                self.line_error[id_list].append(error)
                self.total_errors += 1
                return True
            else:
                return False

    def writeLog(self) -> None:
        def showErrors(message: str) -> str:
            date = datetime.now()
            message = '\n' + '=' * 30 + "\n" + f"{date}\n\n"

            for k, v in self.files.items():
                lines = ", ".join(list(map(lambda x: str(x), self.data[v])))
                message += 'File: "{0}", Error Lines: {1}\n'.format(k, lines)
            return message

        msg = ""
        if self.total_errors == 0:
            msg = '\nAll files, OK!   :)\n\n'
        else:
            msg += showErrors(msg) + '\n'

        if os.path.exists(self.file_error_log):
            with open(self.file_error_log, 'a') as file:
                file.write(msg)
        else:
            with open(self.file_error_log, 'w') as file:
                file.write(msg)

    def __str__(self):
        return f'files: {list(self.files.keys())}, line_errors: {self.data}'
