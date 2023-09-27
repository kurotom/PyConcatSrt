# -*- coding: utf-8 -*-
"""
Tests ReaderFileSrt
"""


from tests_Main import PyConcatSRTTestCase
from src.ReaderFileSrt import ReaderSrt


class ReaderSrtTestCase(PyConcatSRTTestCase):

    def test_ReaderSrt_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            r = ReaderSrt(path='notexist.srt')
            r.process()

    def test_ReaderSrt_dir_not_found(self):
        with self.assertRaises(FileNotFoundError):
            r = ReaderSrt(path='directorynoexist/')
            r.process()
