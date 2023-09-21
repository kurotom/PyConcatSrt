# -*- coding: utf-8 -*-
"""
"""


import re
from datetime import datetime
from typing import Union

from DialogScript import Dialog


class ReadSrt(object):
    def __init__(self, file):
        self.file = file
        self.lines = []
        self.current = 0
        self.dialogsOBJ = []
        self.error_lines = []

    def process(self) -> dict:
        self.__read()

        for i in range(len(self.lines)):
            line = self.lines[i]
            if '-->' in line:
                regex = self.__get_timestamps(line)
                if regex != []:
                    time_tuple = regex[0]
                    if self.__validate_timestamp(time_tuple):
                        self.current = self.__getIndex(i)

                        scriptOBJ = Dialog(
                                    timestamp_start=time_tuple[0],
                                    timestamp_end=time_tuple[1]
                                )
                        scriptOBJ.setPosition(self.__getIndex(i))
                        scriptOBJ.setDialogs(self.__getLines(i + 1))

                        self.dialogsOBJ.append(scriptOBJ)
                    else:
                        self.error_lines.append(self.current)

        return {
            'data': self.dialogsOBJ,
            'errors': self.error_lines
        }

    def __read(self):
        with open(self.file, 'r') as file:
            self.lines = file.readlines()

    def __getIndex(self, current_index) -> int:
        indx = self.lines[current_index - 1].strip()
        if indx.isnumeric():
            return int(indx)
        else:
            return -1

    def __getLines(self, current_index):
        list_dialog = []
        for i in range(current_index, len(self.lines)):
            if self.lines[i].strip() != "":
                list_dialog.append(self.lines[i].strip())
            else:
                break
        return list_dialog

    def __get_timestamps(self, line) -> Union[list, None]:
        reg = r'(\d+:\d{2}:\d{2}\,\d{3}) --> (\d+:\d{2}:\d{2}\,\d{3})'
        regex = re.findall(reg, line)
        return regex

    def __validate_timestamp(self, timestamps: list) -> bool:
        def format(timestamp):
            return timestamp + (15 - len(timestamp)) * '0'

        start = format(timestamps[0])
        end = format(timestamps[1])

        try:
            d1 = datetime.strptime(start, '%H:%M:%S,%f').timestamp()
            d2 = datetime.strptime(end, '%H:%M:%S,%f').timestamp()
            return d2 > d1
        except ValueError as e:
            print('>>>  ', e)
            return False


r = ReadSrt('srts/sample1.srt')
print(r.process())
