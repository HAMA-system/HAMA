import shutil
import time
import re

from FUNC_LIBRARY import xlsxFileController
from HIDDEN_FILES.linkData import *

mem = []
expt = []

def keyword_matching(text, keyword):
    # 월 있으면 한번만 고려하도록
    # print(re.search('[0-9]월',text))
    # print(re.search(keyword,text))

    if re.search(keyword,text) is not None:
        if re.search('[0-9]월',text) is not None:
            return keyword, True
        else:
            return keyword, False
    else:
        return keyword, None


def match():
    print('엑셀파일을 로드하는 중입니다.\n결의내역 또는 결의내역(정기)의 내용이 많을 경우 데이터 로드시간이 1분 이상 소요될 수 있습니다.')

    inputfile = xlsxFileController.load_xls(링크[4]+'bank.xlsx')
    if inputfile is None:
        print("bank.xlsx 파일이 올바르지 않습니다.\n잠시 후 프로그램이 종료됩니다.")
        time.sleep(3)
        return
    bank_sheet_name = inputfile.sheetnames[0]
    input1 = xlsxFileController.all_data_fetch(inputfile,bank_sheet_name,'A9','J9')
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
    next_change = False
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

        checkExpt = True
        prev = input3[-1][1]
        for cont in input3:
            k, r = keyword_matching(line[5], cont[1])
            # print(line[5], cont[1])
            if next_change==True and prev != k:
                # print(prev, k)
                mem.append(prev)
                next_change = False
            if r == True:
                checkExpt = False
                next_change = True
                # print(k, "는 월 포함됨")
                ncont = cont[:6] + cont[7:13]
                # print(ncont)
                xlsxFileController.put_singleline_data_for_bank(output, '결의내역', 'E' + str(i), 'T' + str(i), ncont, line[0])
                i += 1
            elif k not in mem:
                if r is not None:
                    checkExpt = False
                    next_change = True
                    # print(k, "는 그냥")
                    ncont = cont[:6] + cont[7:13]
                    # print(ncont)
                    xlsxFileController.put_singleline_data_for_bank(output, '결의내역', 'E' + str(i), 'T' + str(i), ncont, line[0])
                    i += 1

            prev = k

        # print(mem)
        # print(k, "는 없음")
        # if k not in mem:
        if checkExpt==True:
            expt.append(line[5])
            # print("찾을 수 없음 :", line)

            # if line[5]==cont[1]:
            #     # print(line[5],cont[1])
            #     # print(cont)
            #     ncont = cont[:6] + cont[7:13]
            #     # print(ncont)
            #     xlsxFileController.put_singleline_data_for_bank(output,'결의내역','E'+str(i),'T'+str(i),ncont,line[0])
            #     i += 1
    xlsxFileController.save_xls(output,링크[4]+'afterdata.xlsx')

    E = set(expt)
    print("일치하는 키워드를 찾지 못한 항목이",len(E),"개 있습니다.")
    if expt!=[]:
        print("매칭하지 못한 항목 : ")
        print(*E,sep='\t')
    print("\n모든 작업이 완료되어 5초 후 프로그램이 종료됩니다")
    time.sleep(5)

if __name__ == '__main__':
    match()
    # k, r = keyword_matching('나는 향차이입니다','향차이')
    # if k not in mem:
    #     if r is None:
    #         print(k,"는 없음")
    #     elif r == True:
    #         mem.append(k)
    #         print(k,"는 월 포함됨")
    #     else:
    #         mem.append(k)
    #         print(k,"는 그냥")
    #
    # k, r = keyword_matching('나는 향차이입니다', '향차이')
    # if k not in mem:
    #     if r is None:
    #         print(k, "는 없음")
    #     elif r == True:
    #         mem.append(k)
    #         print(k, "는 월 포함됨")
    #     else:
    #         mem.append(k)
    #         print(k, "는 그냥")

# TODO
# 1. 키워드는 'ㅁㅁㅁ n월' 처럼 몇월로 써지면 중복 허용
# 2. 나머지는 같은 키워드면 중복 무시하고 한번만 작성되도록 (가장 늦은 날짜)
# 3. 공과금으로 작성된 내용은 한번에 작성하고 가장 늦은 날짜로 거래날짜 작성
# 4. 작성되지 않고 넘어간 내용은 콘솔에 뿌려서 확인 가능하게 하기

