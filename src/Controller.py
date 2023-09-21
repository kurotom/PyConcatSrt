# -*- coding: utf-8 -*-
"""
"""

from ReaderFileSrt import ReaderSrt
from WriterFileSrt import WriterSrt
import os


class Control(object):

    def __init__(self):
        self.path = None
        self.data = []
        self.errors_data = []
        self.writer = WriterSrt()
        # self.data = self.reader.process()

    def setPath(self, path):
        if os.path.exists(path):
            self.path = os.path.realpath(path)

    def read(self):
        if self.path is not None:
            errs = []
            if os.path.isfile(self.path):
                self.data = self.__getData(self.path)
                if self.data['error'] != []:
                    derr = {
                            'filename': os.path.basename(self.path),
                            'errors': self.data['error']
                        }
                errs.append(derr)
            elif os.path.isdir(self.path):
                for file in os.listdir(self.path):
                    if file.endswith('srt'):
                        file_path = self.path + f'/{file}'
                        if os.path.exists(file_path):
                            data = self.__getData(file_path)
                            if data['error'] != []:
                                derr = {
                                        'filename': os.path.basename(file),
                                        'errors': data['error']
                                    }
                                errs.append(derr)
                            if data['data'] != []:
                                self.data += data['data']
            self.errors_data = errs
            if len(self.data) > 1:
                self.data = self.__sort_data()
            else:
                return self.data

    def __getData(self, file) -> dict:
        reader = ReaderSrt(file)
        return reader.process()

    def __sort_data(self):
        return sorted(
                self.data,
                key=lambda x: x.getTimestamps()['start']
            )

    def to_write(self, filename):
        self.writer.write(filename, self.convertData())

    def convertData(self):
        indx = 1
        string_script = ""
        for objLine in self.data:
            string_script += "{0}\n{1}\n{2}\n\n".format(
                indx,
                self.__get_timestamps(objLine),
                self.__get_lines(objLine)
            )
            indx += 1
        return string_script

    def __get_timestamps(self, item):
        return "{0} --> {1}".format(item.time_start, item.time_end)

    def __get_lines(self, item):
        return '\n'.join(item.dialog)




c = Control()
c.setPath('25641/')
c.read()
print(c.convertData())
c.to_write('final.srt')
