# -*- coding: utf-8 -*-
"""
Class in charge of reading the srt file or directory that contains multiple srt
files, returning a list of Dialog objects ordered by start time.
"""

import chardet

import re
import os
from typing import Union, List

from src.ErrorClass import ErrorData
from src.DialogScript import Dialog
from src.CheckerSrtFormat import CheckerSrt


class ReaderSrt(object):
    def __init__(
                    self,
                    path: str = None,
                    discs: int = 1,
                    errordata: object = None
                ):
        if errordata is not None:
            self.errorData = errordata
        else:
            self.errorData = ErrorData()

        self.path = path
        self.current = 0
        self.discs = discs

    def process(self) -> List[dict]:
        if os.path.exists(self.path):
            return self.__inner_process()
        else:
            raise FileNotFoundError('File or directory not exists')

    def __inner_process(self) -> List[dict]:
        result = []
        if os.path.isfile(self.path):
            result_lines = self.read_file(self.path)
            current_filename = result_lines['file']
            lines_objs = self.__iterate_lines(
                                        current_filename,
                                        result_lines['data']
                                    )

            result += lines_objs

        elif os.path.isdir(self.path):
            result_lines = self.read_files(self.path)
            if result_lines is None:
                print(f'-->  Directory "{self.path}" does not have SRT files.')
            else:
                if self.discs == 1:
                    for item in result_lines:
                        current_filename = item['file']
                        lines_objs = self.__iterate_lines(
                                                    current_filename,
                                                    item['data']
                                                )
                        result += lines_objs

                elif self.discs == 2:
                    disc1 = self.__iterate_lines(
                                filename=result_lines[0]['file'],
                                data=result_lines[0]['data']
                            )
                    disc2 = self.__iterate_lines(
                            filename=result_lines[1]['file'],
                            data=result_lines[1]['data']
                        )

                    last_entry = disc1[-1]
                    list_updated = self.__update_timestamp(
                                                disc2,
                                                last_entry
                                            )

                    result += disc1
                    result += list_updated

        return result

    def __update_timestamp(self, list_Dialog, objLastDialog) -> list:
        last_entry = objLastDialog
        for item in list_Dialog:
            last_entry = item.update_time(last_entry)
        return list_Dialog

    def __iterate_lines(self, filename: str, data: list) -> List[Dialog]:
        list_dialogsOBJ = []
        error_list = []
        total_lines = len(data)
        for i in range(total_lines):
            line = data[i]
            if '-->' in line:
                regex = self.get_timestamps(line)
                if regex is None:
                    error_list.append(self.getIndex(i, data))
                elif regex != []:
                    time_list = regex[0]
                    if CheckerSrt.validate_timestamp(time_list):
                        self.current = self.getIndex(i, data)

                        lineDialogs = self.getLines(i + 1, data)
                        if lineDialogs != []:
                            scriptOBJ = Dialog(
                                        time_start=time_list[0],
                                        time_end=time_list[1]
                                    )
                            scriptOBJ.setPosition(self.getIndex(i, data))
                            scriptOBJ.setDialogs(lineDialogs)
                            list_dialogsOBJ.append(scriptOBJ)
                        else:
                            self.errorData.registerIndex(
                                            filename,
                                            self.getIndex(i, data)
                                        )
                            self.errorData.registerLine(
                                            filename,
                                            i
                                        )
                    else:
                        self.errorData.registerIndex(
                                        filename,
                                        self.getIndex(i, data)
                                    )
                        self.errorData.registerLine(
                                        filename,
                                        i
                                    )

        return self.__sort_timestamp(list_dialogsOBJ)

    def __sort_timestamp(self, listLineObj: list) -> list:
        return sorted(
                listLineObj,
                key=lambda x: x.getTimestamps()['start']
            )

    def getEncoding(self, filename) -> dict:
        with open(filename, 'rb') as file:
            return chardet.detect(file.read())

    def __read(self, filename, encoding) -> list:
        with open(filename, 'r', encoding=encoding) as file:
            return file.readlines()

    def read_file(self, filename) -> dict:
        file_encoding = self.getEncoding(filename)['encoding']
        data = {
            'file': os.path.basename(filename),
            'data': self.__read(filename, file_encoding)
        }
        return data

    def read_files(self, filename) -> Union[list, None]:
        result = []
        files = sorted(os.listdir(filename))
        files = [i for i in files if i.endswith('.srt')]
        if len(files) > 0:
            for item in files:
                file_path = self.path + f'/{item}'
                if os.path.exists(file_path):
                    file_encoding = self.getEncoding(file_path)['encoding']
                    data = {
                        'file': item,
                        'data': self.__read(file_path, file_encoding)
                    }
                    result.append(data)
            return result
        else:
            return None

    def getIndex(self, current_index, data: list) -> int:
        indx = data[current_index - 1].strip()
        if indx.isnumeric():
            return int(indx)
        else:
            return -1

    def getLines(self, current_index, data: list) -> list:
        list_dialog = []
        for i in range(current_index, len(data)):
            if data[i].strip() != "":
                list_dialog.append(data[i].strip())
            else:
                break
        return list_dialog

    def get_timestamps(self, line) -> Union[list, None]:
        reg = r'(\d+:\d{2}:\d{2}\,\d{3}) --> (\d+:\d{2}:\d{2}\,\d{3})'
        regex = re.findall(reg, line)
        if regex != []:
            return regex
        else:
            return None
