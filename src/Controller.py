# -*- coding: utf-8 -*-
"""
"""

from ReaderFileSrt import ReaderSrt
from WriterFileSrt import WriterSrt
from ErrorClass import ErrorData
import os


class Control(object):

    def __init__(self):
        self.path = None
        self.errors_data = []
        self.writer = WriterSrt()
        self.errorData = ErrorData()

    def setPath(self, path) -> None:
        if os.path.exists(path):
            self.path = os.path.realpath(path)

    def read(self, path: str = None, discs: int = 1) -> list:
        if path is not None:
            try:
                reader = ReaderSrt(path, discs, self.errorData)
                #
                # Si uso solo 'data' para que retornar un diccionario
                # de ReaderSrt.process()  ??????????
                result_data = reader.process()
                size_data = len(result_data)
                if size_data == 1:
                    return self.__sort_data(result_data[0]['data'])
                elif size_data == 2:
                    new = result_data[0]['data'] + result_data[1]['data']
                    return self.__sort_data(new)

            except FileNotFoundError as e:
                return e

    def __sort_data(self, data) -> list:
        return sorted(
                data,
                key=lambda x: x.getTimestamps()['start']
            )

    def to_write(
                    self,
                    filename: str,
                    data: str = None,
                    writeLog: bool = False
                ) -> None:
        if not filename.endswith('.srt'):
            filename = filename + '.srt'

        if data is None:
            self.writer.write(filename, self.convertData())
        else:
            if isinstance(data, str):
                self.writer.write(filename, data)
        if writeLog:
            self.errorData.writeLog()

    def convertData(self, data: list = None) -> str:
        return self.writer.convertData(data)


c = Control()

r = c.read('tests/7809/CD1.srt')
# print(type(r), len(r))
d = c.convertData(r)
c.to_write('single_file.srt', d, writeLog=True)

r = c.read('tests/7809')
# print(type(r), len(r))
d = c.convertData(r)
c.to_write('multi_file_disc_1.srt', d, writeLog=True)
#
r = c.read('tests/7809', 2)
# print(type(r), len(r))
d = c.convertData(r)
c.to_write('multi_file_disc_2', d, writeLog=True)
print(c.errorData)
