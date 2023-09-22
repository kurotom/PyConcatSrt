# -*- coding: utf-8 -*-
"""
"""

import chardet

import re
import os
from datetime import datetime
from typing import Union, List, Dict

from DialogScript import Dialog


class ReaderSrt(object):
    def __init__(self, path: str = None, discs: int = 1):
        self.path = path
        self.lines = []
        self.current = 0
        self.dialogsOBJ = []
        self.error_lines = []
        self.discs = discs
        self.last_time = {
            'last_start': None,
            'last_end': None
        }

    def process(self) -> List[dict]:
        result = []
        if os.path.isfile(self.path):
            if os.path.exists(self.path):
                result_lines = self.__read_file(self.path)
                lines_objs = self.__iterate_lines(result_lines['data'])
                data = {
                    'file': result_lines['file'],
                    'data': lines_objs['data'],
                    'errors': lines_objs['error']
                }
                result.append(data)

        elif os.path.isdir(self.path):
            if os.path.exists(self.path):
                result_lines = self.__read_files(self.path)

                if self.discs == 1:
                    for item in result_lines:
                        lines_objs = self.__iterate_lines(item['data'])
                        data = {
                            'file': item['file'],
                            'data': lines_objs['data'],
                            'errors': lines_objs['error']
                        }
                        result.append(data)
                elif self.discs == 2:
                    disc1 = self.__iterate_lines(result_lines[0]['data'])
                    disc2 = self.__iterate_lines(result_lines[1]['data'])

                    last_entry = disc1['data'][-1]
                    list_updated = self.__update_timestamp(
                                                disc2['data'],
                                                last_entry
                                            )
                    disc1 += list_updated
                    data = {
                        'file': item['file'],
                        'data': disc1,
                        'errors': lines_objs['error']
                    }


        return result

    def __update_timestamp(self, list_Dialog, objLastDialog) -> list:
        last_entry = objLastDialog
        for item in list_Dialog:
            last_entry = item.update_time(last_entry)
        return list_Dialog



    def __iterate_lines(self, data: list) -> dict:
        list_dialogsOBJ = []
        error_list = []
        total_lines = len(data)
        for i in range(total_lines):
            line = data[i]
            if '-->' in line:
                regex = self.__get_timestamps(line)
                if regex is None:
                    error_list.append(self.__getIndex(i, data))
                elif regex != []:
                    time_tuple = regex[0]
                    if self.__validate_timestamp(time_tuple):
                        self.current = self.__getIndex(i, data)

                        lineDialogs = self.__getLines(i + 1, data)
                        if lineDialogs != []:
                            scriptOBJ = Dialog(
                                        time_start=time_tuple[0],
                                        time_end=time_tuple[1]
                                    )
                            scriptOBJ.setPosition(self.__getIndex(i, data))
                            scriptOBJ.setDialogs(lineDialogs)
                            list_dialogsOBJ.append(scriptOBJ)
                        else:
                            error_list.append(self.__getIndex(i, data))
                    else:
                        error_list.append(self.__getIndex(i, data))
        return {
            'data': self.__sort_timestamp(list_dialogsOBJ),
            'error': error_list
        }

    def __sort_timestamp(self, listLineObj: list):
        return sorted(
                listLineObj,
                key=lambda x: x.getTimestamps()['start']
            )


    def __getEncoding(self, filename) -> dict:
        with open(filename, 'rb') as file:
            return chardet.detect(file.read())

    def __read(self, filename, encoding):
        with open(filename, 'r', encoding=encoding) as file:
            return file.readlines()

    def __read_file(self, filename) -> dict:
        file_encoding = self.__getEncoding(filename)['encoding']
        data = {
            'file': os.path.basename(filename),
            'data': self.__read(filename, file_encoding)
        }
        return data

    def __read_files(self, filename) -> list:
        result = []
        files = os.listdir(filename)
        for item in files:
            file_path = self.path + f'/{item}'
            print(file_path)
            if os.path.exists(file_path):
                file_encoding = self.__getEncoding(file_path)['encoding']
                data = {
                    'file': item,
                    'data': self.__read(file_path, file_encoding)
                }
                result.append(data)
        return result


    def __getIndex(self, current_index, data: list) -> int:
        indx = data[current_index - 1].strip()
        if indx.isnumeric():
            return int(indx)
        else:
            return -1

    def __getLines(self, current_index, data: list):
        list_dialog = []
        for i in range(current_index, len(data)):
            if data[i].strip() != "":
                list_dialog.append(data[i].strip())
            else:
                break
        return list_dialog

    def __get_timestamps(self, line) -> Union[list, None]:
        reg = r'(\d+:\d{2}:\d{2}\,\d{3}) --> (\d+:\d{2}:\d{2}\,\d{3})'
        regex = re.findall(reg, line)
        if regex != []:
            return regex
        else:
            return None

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


# # FILE
# r1 = ReaderSrt('7809/CD1.srt', discs=1)
# r1.process()
#
# # DIRECTORY
r2 = ReaderSrt(path='7809', discs=2)
r2.process()
