# -*- coding: utf-8 -*-
"""
"""


class WriterSrt(object):

    def write(self, filename: str = None, data: str = None):
        with open(filename, 'w') as file:
            file.write(data)

    def convertData(self, data: list) -> str:
        indx = 1
        string_script = ""
        for objLine in data:
            print(objLine)
            # string_script += "{0}\n{1}\n{2}\n\n".format(
            #     indx,
            #     self.__format_timestamp(objLine),
            #     self.__get_lines(objLine)
            # )
            # indx += 1
        return string_script

    def __format_timestamp(self, item) -> str:
        print(item)
        # return "{0} --> {1}".format(item.time_start, item.time_end)
        return ''

    def __get_lines(self, item) -> str:
        return '\n'.join(item.dialog)
