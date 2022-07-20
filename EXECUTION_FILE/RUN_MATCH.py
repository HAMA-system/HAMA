import os
from FUNC_LIBRARY import xlsxFileController
from HIDDEN_FILES.linkData import *

def match():
    datafile = xlsxFileController.load_xls(링크[2])
    input2 = xlsxFileController.all_data_fetch(datafile, '결의내역', 'E15', 'X15')

    inputfile = xlsxFileController.load_xls(링크[3]+'HIDDEN_FILES/bank.xlsx')
    input1 = xlsxFileController.all_data_fetch(inputfile,'신한은행_거래내역조회','A9','L9')
    print(input2)
    print(*input1,sep='\n')



if __name__ == '__main__':
    match()