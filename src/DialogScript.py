# -*- coding: utf-8 -*-
"""
Class to convert data on object Dialog with data of dialogs of srt files.
"""


from datetime import datetime


class Dialog(object):
    def __init__(self, time_start, time_end):
        self.line = -1
        self.time_start = time_start
        self.time_end = time_end
        self.dialog = []

    def setPosition(self, line: int):
        if line > 0:
            self.line = line

    def setDialogs(self, list_dialog: list):
        if list_dialog != []:
            self.dialog = list_dialog

    def getTimestamps(self) -> dict:
        return {
                'start': datetime.strptime(
                            self.time_start, '%H:%M:%S,%f'
                        ).timestamp(),
                'end': datetime.strptime(
                            self.time_end, '%H:%M:%S,%f'
                        ).timestamp()
            }

    def __str__(self):
        return "{0} - {1}, {2} => {3}".format(
                self.line,
                self.time_start,
                self.time_end,
                ' '.join(self.dialog)[:10]
            )
