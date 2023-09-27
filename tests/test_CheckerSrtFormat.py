# -*- coding: utf-8 -*-
"""
Tests CheckerSrtFormat
"""

from tests_Main import PyConcatSRTTestCase

from src.CheckerSrtFormat import CheckerSrt


class CheckerSrtFormatTestCase(PyConcatSRTTestCase):

    def setUp(self):
        self.result = [CheckerSrt.validate_timestamp(i) for i in self.mock()]

    def mock(self) -> list:
        return [
            ['00:00:00,000', '00:00:01,000'],
            ['00:10:00,000', '00:00:01,000'],
            ['100:00:00,000', '00:00:01,000'],
            ['00:00:00,000', '00:00:01,000'],
            ['02:00:00,000', '02:00:01,000'],
            ['00:00:00,00034', '00:00:01,00012'],
            ['00:00:00,00011', '00:00:01,000'],
            ['00:00:00,0', '00:00:01,000'],
        ]

    def test_validate_timestamp1(self):
        self.assertEqual(self.result[0], True)

    def test_validate_timestamp2(self):
        self.assertEqual(self.result[1], False)

    def test_validate_timestamp3(self):
        self.assertEqual(self.result[2], False)

    def test_validate_timestamp4(self):
        self.assertEqual(self.result[4], True)

    def test_validate_timestamp5(self):
        self.assertEqual(self.result[5], True)

    def test_validate_timestamp6(self):
        self.assertEqual(self.result[7], True)
