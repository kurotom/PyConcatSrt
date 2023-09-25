# -*- coding: utf-8 -*-
"""
Class in charge of controlling the information workflow between ReaderSrt,
WriterSrt, ErrorData.
"""

from src.ReaderFileSrt import ReaderSrt
from src.WriterFileSrt import WriterSrt
from src.ErrorClass import ErrorData


class Control(object):

    def __init__(self):
        self.path = None
        self.errors_data = []
        self.writer = WriterSrt()
        self.errorData = ErrorData()

    def read(self, path: str = None, discs: int = 1) -> list:
        if path is not None:
            try:
                reader = ReaderSrt(path, discs, self.errorData)
                result_data = reader.process()
                return result_data
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
