# -*- coding: utf-8 -*-
"""
Tests ErrorClass
"""


from tests_Main import PyConcatSRTTestCase

from src.ErrorClass import ErrorData


class ErrorClassTestCase(PyConcatSRTTestCase):

    def setUp(self):
        self.errordata = self.getErrorData()

    def getErrorData(self):
        return ErrorData()

    def mock(self):
        self.errordata.getDataError('name')
        self.errordata.registerIndex('name', [1, 2, 3])
        self.errordata.registerLine('name', [8, 9, 10])

    def test_getDataError_empty_errors(self):
        r = self.errordata.getDataError('name')
        self.assertEqual(r, 0)

    def test_registerIndex(self):
        r = self.errordata.registerIndex('name', [1, 2, 3])
        self.assertEqual(r, True)

    def test_registerLine(self):
        r = self.errordata.registerLine('name', [8, 9, 10])
        self.assertEqual(r, True)

    def test_amount_errors_not_empty_files(self):
        self.mock()
        self.assertGreater(len(self.errordata.files), 0)

    def test_amount_errors_not_empty_data(self):
        self.mock()
        self.assertGreater(len(self.errordata.data), 0)

    def test_amount_errors_not_empty_line_errors(self):
        self.mock()
        self.assertGreater(len(self.errordata.line_error), 0)
