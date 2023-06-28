import sys
import os
import pprint

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from FUNC_LIBRARY import xlsxFileController
from HIDDEN_FILES.linkData import *
from RENEWAL_UTIL import excel, date


""" CONSTANTS """
HIDDENFILE_PATH = 링크[4]
FILE_NAME = "위탁업체/20220407 위탁업체 list.xlsm"  # 파일명
SHEET_NAME = "21년 서울캠"  # 시트명

COLUMNS = ["E", "I", "J", "N", "R"]  # 가져올 열(알파벳)
# 업체명, 시작, 종료, 위탁료(월), 관리비(월)
FIRST_ROW = 5  # 시작 행(숫자)


def run():
    fileName = HIDDENFILE_PATH + "/" + FILE_NAME
    data = excel.read_column_data(fileName, SHEET_NAME, COLUMNS, FIRST_ROW)
    pprint.pprint(excel.remove_none_rows(data))


run()
