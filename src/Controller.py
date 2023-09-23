# -*- coding: utf-8 -*-
"""
"""

from ReaderFileSrt import ReaderSrt
from WriterFileSrt import WriterSrt
# from ErrorClass import ErrorData
import os


class Control(object):

    def __init__(self):
        self.path = None
        self.data = []
        self.errors_data = []
        self.writer = WriterSrt()

    def setPath(self, path) -> None:
        if os.path.exists(path):
            self.path = os.path.realpath(path)

    def read(self, path: str = None, discs: int = 1) -> list:
        if path is not None:
            try:
                reader = ReaderSrt(path, discs)
                result_data = reader.process()
                print(len(result_data))
                for item in result_data:
                    print(item.keys())
                    # self.errorData.filename = item['file']
                    # self.errorData.data = item['error']
                    # data = item['data']
                # return self.__sort_data(reader.process())
            except FileNotFoundError as e:
                return e

    def __sort_data(self, data) -> list:
        return sorted(
                data[0]['data'],
                key=lambda x: x.getTimestamps()['start']
            )

    def to_write(self, filename: str, data: str = None) -> None:
        if not filename.endswith('.srt'):
            filename = filename + '.srt'

        if data is None:
            self.writer.write(filename, self.convertData())
        else:
            if isinstance(data, str):
                self.writer.write(filename, data)

    def convertData(self, data: list = None) -> str:
        for i in self.data:
            print(len(i))
        # if data is None:
        #     return self.writer.convertData(self.data['data'])
        # else:
        #     if isinstance(data, list):
        #         return self.writer.convertData(data)


c = Control()

r = c.read('tests/7809/CD1.srt')
# print(type(r), len(r))
c.convertData(r)
# c.to_write('single_file.srt')

r = c.read('tests/7809')
# print(type(r), len(r))
c.convertData(r)
# c.to_write('multi_file_disc_1.srt')
#
r = c.read('tests/7809', 2)
# print(type(r), len(r))
d = c.convertData(r)
# c.to_write('multi_file_disc_2', d)
