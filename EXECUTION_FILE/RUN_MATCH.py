import shutil
import time
import re

from FUNC_LIBRARY import xlsxFileController
from HIDDEN_FILES.linkData import *

def left_align(text, length, padding=' '):
    from wcwidth import wcswidth
    text = str(text)
    return text + padding * max(0, (length - wcswidth(text)))


def keyword_matching(text, keyword):
    # 월 있으면 한번만 고려하도록
    # print(re.search('[0-9]월',text))
    # print(re.search(keyword,text))
    text = text.replace(' ', '')
    keyword = keyword.replace(' ', '')

    if re.search(keyword, text) is not None:
        if re.search('[0-9]월', text) is not None:
            return keyword, True
        else:
            return keyword, False
    else:
        return keyword, None


def str_eq(str1, str2):
    str1 = str1.replace(' ', '')
    str2 = str2.replace(' ', '')

    if str1 == str2:
        return True
    else:
        return False


def print_similar(bank_list, data_list):
    print("\n* 매칭하지 못한 키워드 중 비슷한 키워드는 다음과 같습니다.")
    print(left_align("[bank.xlsx]", 25) + " -> " + left_align('', 20) + "[data.xlsx]")
    for bank_data in bank_list:
        for data in data_list:
            if re.search(bank_data[5], data[1]) is not None:
                print(left_align("[" + str(bank_data[0]) + "]  " + str(bank_data[5]) + " (" + str(bank_data[4]) + ")", 25)
                      + " -> "
                      + left_align(str(data[1]) + " (" + str(data[2]) + ")", 30) + " [" + str(data[0]) + "]")

###
# 매칭 실패한 내역에 대해 수동으로 찾아서 매칭을 진행시켜주는 함수입니다
# output    : 출력 file stream
# expt      : 매칭 실패한 내역 array
# i         : 현재 입력 중인 행 번호
###
def manual_match(output, expt, i):
    return
    # E = set(expt)
    # print("일치하는 키워드를 찾지 못한 항목이", len(E), "개 있습니다.")
    # print("* 매칭하지 못한 항목")
    # if expt != []:
    #     print(left_align("행번호", 15),
    #           left_align("거래일자", 15),
    #           left_align("시각", 15),
    #           left_align("출금액", 15),
    #           left_align("입금액", 15),
    #           left_align("거래내용", 15))
    #
    #     for row in expt:
    #         print(left_align(row[0], 15) + "\t"
    #               + left_align(row[1], 15) + "\t"
    #               + left_align(row[2], 15) + "\t"
    #               + left_align(row[3], 15) + "\t"
    #               + left_align(row[4], 15) + "\t"
    #               + left_align(row[5], 15))


def match():
    bank_file_name = 'bank.xlsx'
    data_file_name = 'data.xlsx'
    output_file_name = 'afterdata.xlsx'
    path = 링크[4]
    bank_file_path = path + bank_file_name
    data_file_path = path + data_file_name
    output_file_path = path + output_file_name

    # 처리된 부분, 미처리된 부분 기억
    bank_mem = []
    bank_expt = []
    data_mem = []
    data_expt = []

    print('엑셀파일을 로드하는 중입니다.')
    print('결의내역 또는 결의내역(정기)의 내용이 많을 경우 데이터 로드시간이 1분 이상 소요될 수 있습니다.')

    # 엑셀 파일 로딩
    bank_xlsx = xlsxFileController.load_xls(bank_file_path)
    data_xlsx = xlsxFileController.load_xls_d(data_file_path)
    # bank.xlsx 파일이 없음 -> 종료
    if bank_xlsx is None or data_xlsx is None:
        print("입력 파일명이 올바르지 않습니다.")
        print("잠시 후 프로그램이 종료됩니다.")
        time.sleep(3)
        return

    bank_sheet_name = bank_xlsx.sheetnames[0]
    bank_xlsx_data = xlsxFileController.all_data_fetch(bank_xlsx, bank_sheet_name, 'A8', 'J8')
    data_xlsx_period_data = xlsxFileController.all_data_fetch(data_xlsx, '결의내역(정기)', 'E15', 'X15')
    data_xlsx_normal_data = xlsxFileController.all_data_fetch(data_xlsx, '결의내역', 'E15', 'X15')

    output_xlsx = xlsxFileController.load_xls_w(output_file_path)
    # afterdata.xlsx 파일이 없음 -> 복사 및 생성
    if output_xlsx is None:
        print('현재 ' + output_file_name + ' 가 존재하지 않아 '
              + data_file_name + ' 를 복제하여 새로 생성하는 중입니다. 시간이 다소 소요될 수 있습니다.')
        shutil.copyfile(data_file_path, output_file_path)
        output_xlsx = xlsxFileController.load_xls_w(output_file_path)
    print('모든 파일 로드에 성공하였습니다.')

    i = 0
    next_change = False
    for _ in range(len(data_xlsx_normal_data)):
        if data_xlsx_normal_data[i][1] is not None and len(data_xlsx_normal_data[i][1]) < 30:
            i += 1
        else:
            break
    i += 15

    # 결의내역(정기)에서 (행번호, 키워드, 지출) 추출
    data_period_index = 14
    dup_count = 0
    data_size = len(data_xlsx_period_data)
    for data_period_row_num in range(data_size):
        data_period_row = data_xlsx_period_data[data_period_row_num]
        data_period_index += 1

        if data_period_row_num + 1 < data_size and str_eq(data_xlsx_period_data[data_period_row_num + 1][1],
                                                          data_period_row[1]):
            dup_count += 1
            continue

        if type(data_period_row[15]) is float:
            data_mem.append((data_period_index, data_period_row[1], round(data_period_row[15]), dup_count))
        elif type(data_period_row[15]) is int:
            data_mem.append((data_period_index, data_period_row[1], data_period_row[15], dup_count))
        dup_count = 0

    data_period_length = len(data_mem)

    # bank_xlsx_data : bank.xlsx 거래 내역
    for bank_row_num in range(len(bank_xlsx_data)):
        bank_row = bank_xlsx_data[bank_row_num]
        check_expt = True

        for data_row in data_mem:
            if data_row[1] is None or bank_row[5] is None:
                continue

            # 키워드와 금액이 일치하면
            if str(bank_row[5]) == str(data_row[1]) and str(bank_row[4]) == str(data_row[2]):
                bank_mem.append(bank_row)
                data_mem.remove(data_row)
                data_period_index = data_row[0] - 15
                ncont = data_xlsx_period_data[data_period_index][:6] + data_xlsx_period_data[data_period_index][7:13]
                xlsxFileController.put_singleline_data_for_bank(output_xlsx, '결의내역', 'E' + str(i),
                                                                'T' + str(i), ncont, bank_row[0])
                i += data_row[3] + 1
                # print(i, data_row)
                check_expt = False
                break

        if check_expt is True:
            bank_expt.append((bank_row_num + 8, bank_row[0], bank_row[1], bank_row[3], bank_row[4], bank_row[5]))

        ## data_xlsx_period_data : data.xlsx 결의 내역(정기)
        # prev = data_xlsx_period_data[-1][1]
        # for data_period_row in data_xlsx_period_data:
        #     # cont: 결의내역(정기)의 키워드가 없거나 line: 입금자명이 없으면
        #     if data_period_row[1] is None or bank_row[5] is None:
        #         continue
        #
        #     keyword, r = keyword_matching(str(bank_row[5]), str(data_period_row[1]))
        #     if next_change is True and prev != keyword:
        #         # print(prev, k)
        #         bank_mem.append(prev)
        #         data_mem.append(keyword)
        #         next_change = False
        #
        #     if r is True or (keyword not in bank_mem and r is not None):
        #         check_expt = False
        #         next_change = True
        #         # print(k, "는 월 포함됨")
        #         ncont = data_period_row[:6] + data_period_row[7:13]
        #         # print(ncont)
        #         xlsxFileController.put_singleline_data_for_bank(output_xlsx, '결의내역', 'E' + str(i),
        #                                                         'T' + str(i), ncont, bank_row[0])
        #         i += 1
        #     # elif keyword not in bank_mem and r is not None:
        #     #     checkExpt = False
        #     #     next_change = True
        #     #     # print(k, "는 그냥")
        #     #     ncont = data_period_row[:6] + data_period_row[7:13]
        #     #     # print(ncont)
        #     #     xlsxFileController.put_singleline_data_for_bank
        #     #     (output_xlsx, '결의내역', 'E' + str(i), 'T' + str(i), ncont, bank_row[0])
        #     #     i += 1
        #     prev = keyword
        #
        # if check_expt is True:
        #     bank_expt.append((bank_row_num + 9, bank_row[0], bank_row[1], bank_row[3], bank_row[4], bank_row[5]))

    xlsxFileController.save_xls(output_xlsx, output_file_path)

    if data_mem:
        print("\n* 중복을 제외하여 총", str(data_period_length), "개의 내역 중")
        print("일치하는 키워드를 찾지 못한 항목이", len(data_mem), "개 있습니다.\n")
        print("******************** [" +  data_file_name + "] ********************")
        print(left_align("행번호", 6), left_align("키워드", 30), left_align("지출", 11))
        for row in data_mem:
            print(left_align(row[0], 6), left_align(row[1], 30), left_align(row[2], 11))

    bank_expt_length = set(bank_expt)
    if bank_expt:
        print("\n* 총", str(len(bank_xlsx_data)), "개의 내역 중,")
        print("일치하는 키워드를 찾지 못한 항목이", len(bank_expt_length), "개 있습니다.\n")
        print("******************** [" + bank_file_name + "] ********************")
        print(left_align("행번호", 7), left_align("거래일자", 12), left_align("시각", 10),
              left_align("출금액", 11), left_align("입금액", 11), left_align("거래내용", 12))
        for row in bank_expt:
            print(left_align(row[0], 7), left_align(row[1], 12), left_align(row[2], 10),
                  left_align(row[3], 11), left_align(row[4], 11), left_align(row[5], 12))

        print_similar(bank_expt, data_mem)
        # 비슷한 키워드 매칭

    # menu = input("\n수동 입력을 진행하시겠습니까? (0: 종료, 1: 진행) : ")
    # if menu == 1:
    #     manual_match(output_xlsx, bank_expt, i)
    input("\n* 작업을 마치려면 [Enter] 키를 입력하세요. ")

    print("\n모든 작업이 완료되어 5초 후 프로그램이 종료됩니다.")
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