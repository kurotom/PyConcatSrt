# -*- coding: utf-8 -*-
"""
"""


class WriterSrt(object):

    def write(self, filename: str = None, data: str = None):
        with open(filename, 'w') as file:
            file.write(data)
