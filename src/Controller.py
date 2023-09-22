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

    def setPath(self, path):
        if os.path.exists(path):
            self.path = os.path.realpath(path)


    def read(self, path=None) -> list:
        r = []
        if path is not None:
            reader = ReaderSrt(path)
            for item in reader.process():
                # dict_keys(['file', 'data', 'errors'])
                x = self.convertData(item['data'])
                r.append(x)
        return r

    def __sort_data(self):
        return sorted(
                self.data,
                key=lambda x: x.getTimestamps()['start']
            )

    def to_write(self, filename, data):
        pass
        # self.writer.write(filename, self.convertData())

    def convertData(self, data: list) -> str:
        return self.writer.convertData(data)


c = Control()

c.read('7809/CD1.srt')
# print(c.convertData())
# c.to_write('final.srt')
#
#
c.read('7809')
# print(c.convertData())
# c.to_write('final.srt')
