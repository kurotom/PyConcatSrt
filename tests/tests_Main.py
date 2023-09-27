# -*- coding: utf-8 -*-
"""
Tests
"""


import unittest

from src.Controller import Control


class PyConcatSRTTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PyConcatSRTTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.single_file = 'tests/srts/one/sample1.srt'
        self.multi_files_one_disc = 'tests/srts/one/'
        self.multi_files_two_disc = 'tests/srts/three/'
        self.multi_files_two_disc_two_files = 'tests/srts/two/'

        self.getControl_attr = self.getControl()
        self.read_file_one_disc_attr = self.read_file_one_disc()
        self.read_dir_one_disc_attr = self.read_dir_one_disc()
        self.read_dir_two_disc_attr = self.read_dir_two_disc()
        self.read_dir_two_disc_multifiles_attr = self.read_dir_two_disc_multifiles()

    def getControl(self):
        return Control()

    def read_file_one_disc(self):
        control = self.getControl()
        data = control.read(path=self.single_file, discs=1)
        return data

    def read_dir_one_disc(self):
        control = self.getControl()
        data = control.read(path=self.multi_files_one_disc, discs=1)
        return data

    def read_dir_two_disc(self):
        control = self.getControl()
        data = control.read(
                            path=self.multi_files_two_disc_two_files,
                            discs=2
                        )
        return data

    def read_dir_two_disc_multifiles(self):
        control = self.getControl()
        data = control.read(
                            path=self.multi_files_two_disc,
                            discs=2
                        )
        return data
