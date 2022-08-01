import os
import shutil
from FUNC_LIBRARY import xlsxFileController
from HIDDEN_FILES.linkData import *

def match():
    datafile = xlsxFileController.load_xls(링크[2])
    input2 = xlsxFileController.all_data_fetch(datafile, '결의내역', 'E15', 'X15')

    inputfile = xlsxFileController.load_xls(링크[3]+'HIDDEN_FILES/bank.xlsx')
    input1 = xlsxFileController.all_data_fetch(inputfile,'신한은행_거래내역조회','A9','L9')
    print(*input2,sep='\n')
    print(*input1,sep='\n')

    output = xlsxFileController.load_xls(링크[3]+'HIDDEN_FILES/afterdata.xlsx')
    if output is None:
        path = 링크[3]+'HIDDEN_FILES/'
        source = 'data.xlsx'

        destination = 'afterdata.xlsx'
        shutil.copyfile(path + source, path + destination)
        print('현재 afterdata.xlsx 가 존재하지 않아 data.xlsx 를 복제하여 새로 생성하였습니다.')
        output = xlsxFileController.load_xls(링크[3]+'HIDDEN_FILES/afterdata.xlsx')
    print('afetrdata.xlsx 로드에 성공하였습니다.')




if __name__ == '__main__':
    match()