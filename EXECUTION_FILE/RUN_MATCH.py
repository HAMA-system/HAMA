import os
import shutil
from FUNC_LIBRARY import xlsxFileController
from HIDDEN_FILES.linkData import *

def match():
    print('엑셀파일을 로드하는 중입니다.\n결의내역 또는 결의내역(정기)의 내용이 많을 경우 데이터 로드시간이 최대 1분 가량 소요될 수 있습니다.')
    datafile = xlsxFileController.load_xls(링크[2])
    input2 = xlsxFileController.all_data_fetch(datafile, '결의내역', 'E15', 'X15')
    input3 = xlsxFileController.all_data_fetch(datafile, '결의내역(정기)', 'E15', 'X15')

    inputfile = xlsxFileController.load_xls(링크[3]+'HIDDEN_FILES/bank.xlsx')
    input1 = xlsxFileController.all_data_fetch(inputfile,'신한은행_거래내역조회','A9','L9')
    # print(*input2,sep='\n')
    # print(*input1,sep='\n')
    # print(*input3,sep='\n')

    output = xlsxFileController.load_xls(링크[3]+'HIDDEN_FILES/afterdata.xlsx')
    if output is None:
        path = 링크[3]+'HIDDEN_FILES/'
        source = 'data.xlsx'

        destination = 'afterdata.xlsx'
        shutil.copyfile(path + source, path + destination)
        print('현재 afterdata.xlsx 가 존재하지 않아 data.xlsx 를 복제하여 새로 생성하였습니다.')
        output = xlsxFileController.load_xls(링크[3]+'HIDDEN_FILES/afterdata.xlsx')

    print('모든 파일 로드에 성공하였습니다.')

    # for line in input1:
    #     # print(line)
    #     # print(line[5])
    #
    #     for cont in input3:
    #         if line[5]==cont[1]:
    #             print(line[5],cont[1])
    #             xlsxFileController.put_singleline_data(링크[3]+'HIDDEN_FILES/afterdata.xlsx','결의내역(정기)','E15','X15',cont)
    #             xlsxFileController.save_xls(링크[3]+'HIDDEN_FILES/afterdata.xlsx')



if __name__ == '__main__':
    match()