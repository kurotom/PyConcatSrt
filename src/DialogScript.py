# -*- coding: utf-8 -*-
"""
Class to convert data on object Dialog with data of dialogs of srt files.
"""


class Dialog(object):
    def __init__(self, timestamp_start, timestamp_end):
        self.line = -1
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.dialog = []

    def setPosition(self, line: int):
        if line > 0:
            self.line = line

    def setDialogs(self, string_dialog: list):
        self.dialog.append(string_dialog)

    def __str__(self):
        return "{0} - {1}, {2} => {3}".format(
                self.line,
                self.timestamp_start,
                self.timestamp_end,
                ' '.join(self.dialog)[:10]
            )
