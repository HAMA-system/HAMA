import os
import shutil
from FUNC_LIBRARY import xlsxFileController
from HIDDEN_FILES.linkData import *

def match():
    print('엑셀파일을 로드하는 중입니다.\n결의내역 또는 결의내역(정기)의 내용이 많을 경우 데이터 로드시간이 1분 이상 소요될 수 있습니다.')

    inputfile = xlsxFileController.load_xls(링크[4]+'bank.xlsx')
    input1 = xlsxFileController.all_data_fetch(inputfile,'신한은행_거래내역조회','A9','L9')
    # print(*input2,sep='\n')
    # print(*input1,sep='\n')
    # print(*input3,sep='\n')
    # input2 = xlsxFileController.all_data_fetch(inputfile, '결의내역', 'E15', 'X15')

    output = xlsxFileController.load_xls_w(링크[4]+'afterdata.xlsx')
    if output is None:
        print('현재 afterdata.xlsx 가 존재하지 않아 data.xlsx 를 복제하여 새로 생성하는 중입니다. 시간이 다소 소요될 수 있습니다.')
        # datafile = xlsxFileController.load_xls(링크[2])

        path = 링크[4]
        source = 'data.xlsx'

        destination = 'afterdata.xlsx'
        shutil.copyfile(path + source, path + destination)
        output = xlsxFileController.load_xls_w(링크[4]+'afterdata.xlsx')

    input3 = xlsxFileController.all_data_fetch(output, '결의내역(정기)', 'E15', 'X15')
    print('모든 파일 로드에 성공하였습니다.')

    input2 = xlsxFileController.all_data_fetch(output, '결의내역', 'E15', 'X15')

    i = 0
    for _ in range(len(input2)):
        # print(input2[i][0])
        if input2[i][1] is not None and len(input2[i][1])<30:
            i += 1
        else:
            break
    i += 15
    for line in input1:
        # print(line)
        # print(line[5])

        for cont in input3:
            if line[5]==cont[1]:
                # print(line[5],cont[1])
                # print(cont)
                ncont = cont[:6] + cont[7:13]
                # print(ncont)
                xlsxFileController.put_singleline_data_for_bank(output,'결의내역','E'+str(i),'T'+str(i),ncont,line[0])
                i += 1
    xlsxFileController.save_xls(output,링크[4]+'afterdata.xlsx')



if __name__ == '__main__':
    match()