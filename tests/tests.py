# -*- coding: utf-8 -*-
"""
"""


from src.Controller import Control

c = Control()
#
# r = c.read('tests/7809/CD1.srt')
# print(type(r), len(r))
# d = c.convertData(r)
# c.to_write('single_file.srt', d, writeLog=True)
#
# r = c.read('tests/7809')
# print(type(r), len(r))
# d = c.convertData(r)
# c.to_write('multi_file_disc_1.srt', d, writeLog=True)
# #
# r = c.read('tests/7809', 2)
# print(type(r), len(r))
# d = c.convertData(r)
# c.to_write('multi_file_disc_2', d, writeLog=True)
# # print(c.errorData)
#
#
# r = c.read('tests/srts/sample1.srt')
# print(type(r), len(r))
# d = c.convertData(r)
# c.to_write('single_file.srt', d, writeLog=True)
#
r = c.read('tests/srts/')
print(type(r), len(r))
d = c.convertData(r)
c.to_write('multi_file_disc_1.srt', d, writeLog=True)
