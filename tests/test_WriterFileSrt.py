# -*- coding: utf-8 -*-
"""
Tests WriterFileSrt
"""

from tests_Main import PyConcatSRTTestCase

from src.WriterFileSrt import WriterSrt
from src.DialogScript import Dialog
from random import randint


class WriterFileSrtTestCase(PyConcatSRTTestCase):

    def setUp(self):
        self.data = self.mock()

    def mock(self) -> list:
        def r_n():
            return randint(0, 10)

        r = []
        for i in range(5):
            time = f'0{r_n()}:{r_n()}{r_n()}:0{r_n()},{r_n()}{r_n()}{r_n()}'
            dialog = Dialog(time_start=time, time_end=time)
            dialog.setDialogs(['hi\n', 'bye\n'])
            r.append(dialog)
        return r

    def getWriter(self) -> WriterSrt:
        return WriterSrt()

    def test_convertData(self):
        writer = self.getWriter()
        r = writer.convertData(self.data)
        self.assertEqual(type(r), str)
        self.assertGreater(len(r), 0)

    def test_convertData_empty(self):
        writer = self.getWriter()
        r = writer.convertData('')
        self.assertEqual(r, '')
