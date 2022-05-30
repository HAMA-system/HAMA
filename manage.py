import os
import re
import sys
import time

import autoLogin
import dateController
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains

import hotKeyManager
from autoLogin import *
from linkData import *
from alertController import *
from hotKeyManager import *
from copy import deepcopy
import xlsxFileController
import ignoreAutoLogout
import threading
import asyncio

sema = 0
d = ''
mod_month = "-1"
tax_date = []
res = []
def refresh():
    # TODO
    #   작성에서도 되게 바꿔야 함.
    cpath(d,조회)

def printProgress(i, max):
    c = int(i*max)
    sys.stdout.write('\r[' + '#'*c + ' '*(max-c-1) + ']\t\t[' + str(int(i*100)) + '%]')

def monthly_textReplace(prev,month):
    r = re.compile('(\D*)([\d,]*\d+)(월)(\D*)')
    text_list = prev.split()
    result_string = ""

    for p in text_list:
        # print(p)
        m = r.match(p)
        if m:
            # print(m)
            result_string += re.sub('(\D*)([\d,]*\d+)(월)(\D*)', '\g<1>' + month + '\g<3>\g<4> ', p)
        else:
            result_string += p + " "

    print(result_string)
    return result_string

def dorm(driver, dep, pop):
    fpath(driver, dep, '')
    epath(driver, dep)

    try:
        driver.switch_to.alert.accept()
    except:
        driver.switch_to.frame('frmPopup')
        epath(driver, pop)
        fpath(driver, 소속코드, 'A33100')
        epath(driver, 소속코드)
        time.sleep(0.3)
        actions = ActionChains(driver)
        doubleClick = driver.find_element_by_xpath(소속테이블)
        actions.move_to_element(doubleClick)
        actions.double_click(doubleClick)
        actions.perform()
        driver.switch_to.default_content()
        driver.switch_to.frame('ifr_d4_AHG020P')

def lookup(driver):
    global sema
    global d
    d = driver
    ig = threading.Thread(target=ignoreAutoLogout.startTimer)
    ig.daemon = True
    ig.start()
    driver.switch_to.default_content()
    cpath(driver,결의서_조회)
    driver.switch_to.frame(조회_프레임)

    while True:
        while True:
            ignoreAutoLogout.timer = 0
            sema = 0
            print("회계 구분번호를 입력해주세요. ex) 1(등록금)/2(비등록금)/0(뒤로가기) ")
            acc = input().strip()
            if acc == '1' or acc == '2' or acc == '3':
                break
            print("잘못된 입력입니다.")
        if acc == '0':
            driver.switch_to.default_content()
            return
        while True:
            sema = 1
            print("결의서 구분번호를 입력해주세요. ex) 1(전체)/2(수입)/3(지출)/4(대체)")
            res = input().strip()
            # TODO
            #   modify처럼 형식 변경 필요
            if res == '1' or res == '2' or res == '3' or res == '4':
                break
            print("잘못된 입력입니다.")

        while True:
            print("원하시는 기간을 선택하세요. ex) 1/3/6/12/2022")
            month = input().strip()
            if len(month) == 1 or len(month) == 2 or len(month) == 4:
                break
            print("잘못된 입력입니다.")
        print("원하는 검색어를 입력해주세요. (없으면 공백)")
        search = input().strip()

        if len(month) == 4:
            fname(driver,'txtSAcctYear',month)
        else:
            fname(driver,'txtSAcctYear','2021')
        select = Select(driver.find_element_by_xpath(회계구분_조회))
        if acc == '1':
            select.select_by_index(0)
        elif acc == '2':
            select.select_by_index(1)

        select = Select(driver.find_element_by_xpath(결의서구분))
        if res == '1':
            select.select_by_index(0)
        elif res == '2':
            select.select_by_index(1)
        elif res == '3':
            select.select_by_index(2)
        elif res == '4':
            select.select_by_index(3)

        if month == '1':
            fname(driver,'DpFrDt',dateController.date1month())
        elif month == '3':
            fname(driver,'DpFrDt',dateController.date3month())
        elif month == '6':
            fname(driver,'DpFrDt',dateController.date6month())
        elif month == '12':
            fname(driver,'DpFrDt',dateController.date1year())
        elif len(month) == 4:
            fname(driver,'DpFrDt',month+'0301')
            fname(driver,'DpToDt',str(int(month)+1)+'0228')

        elif month == '종료':
            break
        else:
            print("잘못된 입력입니다.")
        if len(month) != 4:
            fname(driver,'DpToDt',dateController.dateToday())
        fpath(driver,제목_검색,search)
        cname(driver,'CSMenuButton1$List')
        print("\n=====================================================")

def write(driver):
    # TODO
    #   해결할 것 :
    #   거래처 코드 11 처럼 두자리면 클릭해야함
    #   렉 걸릴때 처리할 것 추가
    #   추가 할 것 :
    #   i 유지 코드
    #   가서 여러줄 받고 돌아오게 하기
    #   속도 느린지 빠른지 체크해서 fpath에 time.sleep(n)

    try:

        driver.switch_to.default_content()
        cpath(driver,결의서_작성)
        driver.switch_to.frame(작성_프레임)
        # progress = 0.0
        # progrexx_max = xlsxFileController.get_max_row(file,'결의내역','E')
        # progress_size = 30

        print("\n\n\n=================================")
        while True:
            print("결의서를 작성하시겠습니까? 1(예)/2(아니오)")
            yes = input()
            if yes == '1':
                break

        file = xlsxFileController.load_xls(링크[2])
        input_data = xlsxFileController.all_data_fetch(file,'결의내역','E15','X15')
        # monthly_data = xlsxFileController.all_data_fetch(file,'결의내역(정기)','E15','W15')
        w = 0
        prev = input_data[0][0]
        tax = 0

        target_data = input_data
        row = 15
        isMonthly = False
        # Main loop
        for i in range(len(target_data)):
            if target_data[i][0] != -1 or prev != -1:
                w = 1
                if prev != target_data[i][0]:
                    if tax == 1:
                        file = taxWrite(driver, prev, file, isMonthly, row)
                        tax = 0
                    row = 15 + i
                    isMonthly = False

                    save(driver)
                    if target_data[i][0] == -1:
                        prev = target_data[i][0]
                        continue

                    upload(driver, prev)
                    cpath(driver,신규)
                    # for p in range(len(target_data)):
                    #     if target_data[p][0] == prev:
                    #         xlsxFileController.put_cell_data(file, '결의내역', 'E'+str(p+15), -1)
                    time.sleep(0.5)

                    print("구분번호 :", target_data[i][0])

                print(i + 15, '행 입력중입니다.', sep='')

                # 정기 체크
                if target_data[i][1] is not None and target_data[i][1] != '' and target_data[i][1] != '_':
                    isMonthly = True
                    target_data[i][18] = str(target_data[i][18])
                    target_data[i][2] = str(target_data[i][2])
                    target_data[i][18] = monthly_textReplace(target_data[i][18], target_data[i][2])

                    if target_data[i][3] is not None and target_data[i][3] != '' and target_data[i][3] != '_':
                        target_data[i][3] = monthly_textReplace(str(target_data[i][3]), target_data[i][2])


                # sys.stdout.flush()
                # printProgress(progress/progrexx_max, progress_size)
                # progress += progress/progrexx_max
                time.sleep(0.5)
                if target_data[i][4] is not None and target_data[i][4] != '' and target_data[i][4] != '_':
                    target_data[i][4] = str(target_data[i][4])[:10]
                    # if target_data[i][2][:4] != '2022':
                    #     time.sleep(1)
                    #     fpath(driver, 회계년도, target_data[i][2][:2])
                    #     fpath(driver, 'txtSAcctYear', target_data[i][2][:4])
                    #     time.sleep(5000)
                    #     time.sleep(0.2)
                time.sleep(0.2)
                select = Select(driver.find_element_by_xpath(회계구분_작성))
                if target_data[i][5] is not None and target_data[i][5] != '' and target_data[i][5] != '_':
                    if target_data[i][5] == '등록금':
                        select.select_by_index(0)
                    elif target_data[i][5] == '비등록금' or target_data[i][5] == '(서울)기숙사':
                        select.select_by_index(1)
                    time.sleep(0.2)

                if target_data[i][4] is not None and target_data[i][4] != '' and target_data[i][4] != '_':
                    fpath(driver,결의일자_번호,target_data[i][4])
                select = Select(driver.find_element_by_id('ddlResolutionDiv'))
                if target_data[i][6] is not None and target_data[i][6] != '' and target_data[i][6] != '_':
                    test3 = {"수입" : 0, "지출" : 1, "대체" : 2}
                    select.select_by_index(test3[target_data[i][6]])

                    fpath(driver,사업코드,target_data[i][5])
                    epath(driver,사업코드)
                    driver.switch_to.frame('frmPopup')
                    epath(driver,사업팝업)
                    driver.switch_to.default_content()
                    driver.switch_to.frame('ifr_d4_AHG020P')
                if target_data[i][3] is not None and target_data[i][3] != '' and target_data[i][3] != '_':
                    fpath(driver,결의서_제목,target_data[i][3])
                fpath(driver,계정과목,target_data[i][8])
                epath(driver,계정과목)

                if target_data[i][9] is not None and target_data[i][9] != '' and target_data[i][9] != '_':
                    time.sleep(0.1)
                    fpath(driver,관리코드,target_data[i][9])
                    time.sleep(0.1)
                    epath(driver,관리코드)
                    time.sleep(0.2)
                    try:
                        driver.switch_to.alert.accept()
                    except:
                        driver.switch_to.frame('frmPopup')
                        epath(driver,관리팝업)
                        time.sleep(0.2)
                        driver.switch_to.default_content()
                        driver.switch_to.frame('ifr_d4_AHG020P')

                if target_data[i][11] is not None and target_data[i][11] != '' and target_data[i][11] != '_':
                    if target_data[i][11] == '기숙사':
                        dorm(driver, 귀속부서, 귀속부서팝업)
                    else:
                        fpath(driver, 귀속부서, target_data[i][11])
                        epath(driver, 귀속부서)

                if target_data[i][12] is not None and target_data[i][12] != '' and target_data[i][12] != '_':
                    if target_data[i][12] == '기숙사':
                        dorm(driver, 예산부서, 예산부서팝업)
                    else:
                        fpath(driver, 예산부서, target_data[i][12])
                        epath(driver, 예산부서)

                select = Select(driver.find_element_by_id('ddlDetailEvidenceGb'))

                test2 = {"없음" : 0, "세금" : 1, "기타" : 2, "현금" : 3}
                select.select_by_index(test2[target_data[i][13]])

                if target_data[i][16] is not None and target_data[i][16] != '' and target_data[i][16] != '_':
                    fpath(driver,지출,target_data[i][16])
                if target_data[i][17] is not None and target_data[i][17] != '' and target_data[i][17] != '_':
                    fpath(driver,수입,target_data[i][17])
                if target_data[i][18] is not None and target_data[i][18] != '' and target_data[i][18] != '_':
                    fpath(driver,적요,target_data[i][18])

                time.sleep(0.2)
                cpath(driver,결의내역_제출)
                time.sleep(0.3)

                if target_data[i][13] == '세금':
                    tax = 1
                    dismissAlert(driver)

            prev = target_data[i][0]

            if i == len(target_data)-1 and w == 1:
                if tax == 1:
                    file = taxWrite(driver, target_data[i][0], file, isMonthly, row)
                    tax = 0

                save(driver)
                upload(driver, prev)

                # for p in range(len(target_data)):
                #     if target_data[p][0] == prev:
                #         xlsxFileController.put_cell_data(file, '결의내역', 'E' + str(p+15), -1)
                print("입력이 완료되었습니다.")
                print("구분번호 미변경시 중복 입력될 수 있으니 확인 부탁드립니다.")
                # xlsxFileController.save_xls(file)
        # delete(file)

    except:
        print('오류가 발생하여 초기화면으로 돌아갑니다')
        # driver.refresh()
        autoLogin.afterLogin(driver)
        # xlsxFileController.save_xls(file)



def taxWrite(driver, num, file, isMonthly, row):
    time.sleep(0.3)
    cpath(driver, 세금계산_탭)
    tax_data = xlsxFileController.all_data_fetch(file, '결의내역', 'AB' + str(row), 'AJ' + str(row))
    for j in range(len(tax_data)):
        if tax_data[j][0] == num:
            test = {"매입세금-불" : 1, "매입세금" : 2, "매입계산" : 3, "매출세금" : 4, "매출계산" : 5,
                    "매출세금-불" : 6, "수입세금" : 7, "수입계산" : 8, "매입세금-간" : 9}
            select = Select(driver.find_element_by_xpath(과세구분))
            select.select_by_index(test[tax_data[j][1]])
            fpath(driver, 발행일자, tax_data[j][2].strftime("%Y%m%d"))
            epath(driver, 발행일자)
            fpath(driver, 거래처, '')
            epath(driver, 거래처)
            time.sleep(0.5)  # 없어도 돌아가긴 함
            driver.switch_to.frame('frmPopup')
            if 48 <= ord(str(tax_data[j][3])[0]) <= 57:
                fpath(driver, 사업자번호, tax_data[j][3])
                epath(driver, 사업자번호)
            else:
                fpath(driver, 거래처명, tax_data[j][3])
                epath(driver, 거래처명)
            driver.switch_to.default_content()
            driver.switch_to.frame('ifr_d4_AHG020P')
            if tax_data[j][4] is not None and tax_data[j][4] != '' and tax_data[j][4] != '_':
                fpath(driver, 공급가액, tax_data[j][4])
                fpath(driver, 세액, tax_data[j][5])

            select = Select(driver.find_element_by_id('ddlBillDiv'))
            test1 = {"일반" : 1, "전자" : 2, "현금" : 3}
            select.select_by_index(test1[tax_data[j][6]])
            cpath(driver, 세금계산_제출)
            time.sleep(0.5)
    # for p in range(len(tax_data)):
    #     if tax_data[p][0] == num:
    #         if isMonthly:
    #             xlsxFileController.put_cell_data(file, '결의내역', 'AB' + str(p+row), -1)
    #         else:
    #             xlsxFileController.put_cell_data(file, '세금계산', 'E' + str(p+20), -1)
    cpath(driver, 결의내역_탭)
    print("세금처리가 완료되었습니다.")
    return file

def upload(driver, num):
    path = 링크[3] + str(num) + '/'
    exist = 0
    for x in os.listdir(링크[3]):
        if x == str(num):
            exist = 1
            break
    if exist:
        cpath(driver, 첨부파일)
        driver.switch_to.window(driver.window_handles[1])
        for f in os.listdir(path):
            driver.find_element_by_xpath(파일선택).send_keys(path + f)
            time.sleep(0.3)
            cpath(driver, 파일업로드)
            print(f, "파일 업로드 완료")

        # 나중에 조정해야함
        time.sleep(0.5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.1)
        driver.switch_to.frame(작성_프레임)
        cpath(driver, 저장)
        time.sleep(0.3)
        dismissAlert(driver)

def save(driver):
    while True:
        print("저장하시겠습니까? 1(예)/ 2(아니오)")
        sv = input()
        # sv = '1'
        if sv == '1':
            break
        else:
            time.sleep(3)

    cpath(driver,저장)
    time.sleep(0.3)
    acceptAlert(driver)

def delete(file):
    print("입력된 데이터를 전부 삭제하겠습니까? 1(예)/2(아니오)")
    d = input().strip()
    if d == '1':
        xlsxFileController.delete_completed_row(file, '결의내역', 'E', 'Y', 15)
        xlsxFileController.delete_completed_row(file, '세금계산', 'E', 'L', 20)
        # xlsxFileController.save_xls(file)
        print("삭제가 완료되었습니다.")

def modify(driver):
    global sema
    global d
    d = driver
    ig = threading.Thread(target=ignoreAutoLogout.startTimer)
    ig.daemon = True
    ig.start()

    hotkey_thread = threading.Thread(target=hotKeyManager.hotkeyStart)
    hotkey_thread.daemon = True
    hotkey_thread.start()

    cpath(driver,결의서_조회)

    # TODO
    #   년도 바뀌는 것 생각
    #   실제 케이스 :
    #       0. ~~~ 4월 // +1 해도 되면 예외케이스 5. 문제 X, 일단 +1 하는 것으로 선정
    #       0. ~~~ 4,5월 -> 6,7,8월 // 가능?
    #   예외 케이스 :
    #       1. 12월 ~ 3월 ( x월 ~ y월 -> y월 ~ 2*y-x월 , % 고려 필수 )
    #       2. 2,3월 인데 2월 따로 3월 따로
    #       3. 22.6.7 ~ 22.9.6 (양옆에 . 확인)
    #       4. 22/04/07 ( 고려 할 필요 X )
    #       5. 4월 4월 3월 ( 무조건 +1, n월 발견시 n+1월)
    #   고려 할 것 :
    #       03월, 3월, 10월 다르니 월 앞 두번째 받아 숫자면 이용
    #       1년 지나갈 수 있음
    #   처리해야 할 순서 :
    #       1) +1로 변경 ㅇㄹ
    #       2) 다양한 월 케이스 인식 ㅇㄹ
    #       3) 분기 넘어 갈 때 % 처리 ㅇㄹ
    #       4) 분기데이터는 결의일자 +n
    #   ValueError: invalid literal for int() with base 10: '4월'

    while True:
        modify_input()
        # month = modify_input()
        # print("\n결의서 클릭이 완료되면 엔터를 눌러주세요")
        # input()

        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)
        driver.switch_to.frame('frmPopup')

        # 결의서 제목 및 날짜 저장
        title = []
        res_date = driver.find_element_by_xpath(결의일자_번호)
        title.append(res_date.get_attribute("value"))
        res_title = driver.find_element_by_xpath(결의서_제목)
        title.append(res_title.get_attribute("value"))

        # TODO 예외 케이스 있는지 확인 해볼것, 함수화
        # 결의서 날짜 변경
        change = str(int(title[0][5:7])%12 + 1)
        if int(change) < 10:
            change = "0" + change
        title[0] = title[0][:5] + change + title[0][7:]

        # 달마다 없는 날짜 처리
        if int(change) == 1:
            if int(title[0][8:]) > 28:
                title[0] = title[0][:8] + str(28)
        if int(title[0][8:]) == 31:
            if int(change) != 7:
                title[0] = title[0][:8] + str(30)

        # 복사 창 이동
        cpath(driver, 복사)
        alert = driver.switch_to.alert
        alert.send_keys(title[0])
        for _ in range(3):
            acceptAlert(driver)

        # 내부 데이터 수집 (결의항목)
        table = driver.find_element_by_xpath(결의서_테이블)
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        for tr in tbody.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            i = 0
            for td in tr.find_elements(by=By.TAG_NAME, value="td"):
                i += 1
                if i == 10:
                    res.append(td.get_attribute("innerText"))

        # 내부 데이터 수집 (세금)
        table = driver.find_element_by_xpath(세금계산_테이블)
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        tax_date = []
        for tr in tbody.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            i = 0
            for td in tr.find_elements(by=By.TAG_NAME, value="td"):
                i += 1
                if i == 4:
                    tax_date.append(td.get_attribute("innerText"))


        # 불필요한 띄어쓰기 제거
        # title[1] = monthly_textReplace(title[1], month).rstrip()
        next_month, next_value = monthly_check(title[1])
        title[1] = monthly_next(title[1],next_month,next_value)
        for i in range(len(res)):
            res[i] = monthly_next(res[i], next_month, next_value)
            # res[i] = monthly_textReplace(res[i], month).rstrip()
        print("결의서 날짜 + 제목", title, "", "적요", *res,"", sep='\n')

        # 날짜 및 제목 입력
        time.sleep(0.5)
        fpath(driver, 집행요청일, title[0])
        epath(driver, 집행요청일)

        time.sleep(0.5)
        fpath(driver, 지급예정일, title[0])
        epath(driver, 지급예정일)
        acceptAlert(driver)

        fpath(driver,결의서_제목, title[1])
        driver.find_element_by_xpath(세부사항).clear()

        # 결의서 작성
        for i in range(len(res)):
            cpath(driver, 결의서_링크 + '['+str(i+2)+']')
            fpath(driver, 적요, res[i])
            cpath(driver, 결의내역_제출)
            time.sleep(0.1)

        # 세금 작성
        if tax_date and tax_date[0] != '':
            cpath(driver, 세금계산_탭)

            # TODO 함수화
            # 세금 날짜 변경
            for i in range(len(tax_date)):
                change = str(int(tax_date[i][5:7]) % 12 + 1)
                if int(change) < 10:
                    change = "0" + change
                tax_date[i] = tax_date[i][:5] + change + tax_date[i][7:]

                # 달마다 없는 날짜 처리
                if int(tax_date[i][8:]) == 31:
                    if int(change) == 1:
                        tax_date[i] = title[i][:8] + str(28)
                    elif int(change) != 7:
                        tax_date[i] = tax_date[i][:8] + str(30)

            print("세금 날짜", *tax_date, "",sep='\n')

            # 세금 작성
            for i in range(len(tax_date)):
                cpath(driver, 세금계산_링크 + '['+str(i+2)+']')
                fpath(driver, 발행일자, tax_date[i])
                cpath(driver, 세금계산_제출)
                time.sleep(0.1)
            cpath(driver,결의내역_탭)

        print("작성되었습니다.\n저장하시겠습니까? 1(예)/2(아니오)")
        s = input()
        if s == '1':
            cpath(driver, 저장)
            time.sleep(1)
            dismissAlert(driver)
            print("저장이 완료되었습니다.")
            time.sleep(2)
            driver.switch_to.default_content()
            driver.switch_to.frame(조회_프레임)
            cpath(driver,닫기)

        else:
            print("창을 닫고 재시작을 원하시면 1 입력해주세요")
            while input() != '1':
                print("잘못된 입력입니다.")
            driver.switch_to.default_content()
            driver.switch_to.frame(조회_프레임)
            cpath(driver,닫기)
        time.sleep(1)

        print("\n=====================================================")


def monthly_check(prev):
    r = re.compile('(\D*)([\d,]*\d+)(월)(\D*)')
    n = re.compile(('\d[ , ]+\d'))
    q = re.compile(('~'))
    y = re.compile('(\d*)(년)')

    # Key : 0 == 일반적인 케이스 / 1 == 연속된 달 / 2 == 분기
    l, key = 0, 0
    ret = []
    ret_y = []
    if n.search(prev):
        key = 1
    if q.search(prev):
        key = 2

    text_list = prev.split()
    pprev = ""
    for p in text_list:
        if y.match(pprev) and r.match(p):
            # print(int(p[:-1]))
            temp = []
            m = l
            x = []
            while m < l + len(p):
                if '0' <= prev[m] <= '9':
                    s = prev[m]
                    if '0' <= prev[m + 1] <= '9':
                        s += prev[m + 1]
                        m += 1
                    # ret.append(s)
                    x.append(int(s))
                m += 1
            for tmp in temp:
                if tmp not in ret:
                    x.append(int(s))
            ret_y.append([int(pprev[:-1]),x])
        elif r.match(p):
            # TODO 임시 처리
            temp = []
            m = l
            while m < l + len(p):
                if '0' <= prev[m] <= '9':
                    s = prev[m]
                    if '0' <= prev[m+1] <= '9':
                        s += prev[m+1]
                        m += 1
                    # ret.append(s)
                    temp.append(s)
                m += 1
            for tmp in temp:
                if tmp not in ret:
                    ret.append(tmp)

        l += len(p)+1
        pprev = p
    return ret, key, ret_y

# TODO
#   /d/d? 꼴로 바꾸기
def monthly_textReplace(prev, month):
    r = re.compile('(\D*)([\d,]*\d+)(월)(\D*)')
    text_list = prev.split()
    result_string = ""

    for p in text_list:
        m = r.match(p)
        if m:
            result_string += re.sub('(\D*)([\d,]*\d+)(월)(\D*)', '\g<1>' + month + '\g<3>\g<4> ', p)
        else:
            result_string += p + " "

    return result_string

def modify_input():
    print("변경하실 페이지를 띄우신 후 엔터를 눌러주세요")
    input()

    # global mod_month
    # while True:
        # print("변경하실 페이지를 띄우신 후 변경하실 월을 입력해주세요")
        # print("변경하실 월을 입력해주세요")
        # month = input()
        # if re.fullmatch(r'(\D*)([\d,]*\d+)', month):
        #     break
        # print("잘못된 입력입니다.")
    # mod_month = month
    # return month

def find_res():
    global d
    driver = d
    print("res thread start")
    table = driver.find_element_by_xpath(
        '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/div[1]/div/div/table')
    tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    while res:
        res.pop()
    test = 0
    for tr in tbody.find_elements(by=By.TAG_NAME, value="tr"):
        i = 0
        for td in tr.find_elements(by=By.TAG_NAME, value="td"):
            i += 1
            print(td.get_attribute("innerText"), end='\t')
            if i == 10:
                res.append(td.get_attribute("innerText"))
        print()
        test += 1
    print()
    print("res thread end",res)
    return
    # ft = threading.Thread(target=find_tax)
    # ft.daemon = True
    # ft.start()

def find_tax():
    global d
    driver = d
    "tax thread start"
    table = driver.find_element_by_xpath(
        '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[3]/div/div[1]/div')
    tbody = table.find_element(by=By.TAG_NAME, value="tbody")
    while tax_date:
        tax_date.pop()
    for tr in tbody.find_elements(by=By.TAG_NAME, value="tr"):
        i = 0
        for td in tr.find_elements(by=By.TAG_NAME, value="td"):
            i += 1
            print(td.get_attribute("innerText"), end='\t')
            if i == 4:
                tax_date.append(td.get_attribute("innerText"))
        print()
    print()

def month_inc(month, val):
    ret = []
    for m in month:
        nm = int(m)+val
        if nm > 12:
            nm %= 12
        ret.append(str(nm))
    return ret

def ymonth_inc(ymonth, val):
    ret = []
    for m in ymonth[1]:
        nm = m+val
        if nm > 12:
            nm %= 12
            ymonth += 1
        ret.append(nm)
    return ret

def monthly_next(prev, month, val, ymonth):
    cmonth = deepcopy(month)
    cymonth = deepcopy(ymonth)
    n = len(prev)
    s = ""
    # 일반적 케이스
    for m in cmonth:
        if val == 0:
            # %d월 확인
            next_month = month_inc(cmonth, 1)
            for i in range(len(cmonth)):
                cmonth[i] = int(cmonth[i])
                next_month[i] = int(next_month[i])
            cmonth.sort(reverse=True)
            next_month.sort(reverse=True)
            for i in range(len(cmonth)):
                cmonth[i] = str(cmonth[i])
                next_month[i] = str(next_month[i])
            for i in range(len(cmonth)):
                cmonth[i] += "월"
                next_month[i] += "월"
            for i in range(len(cmonth)):
                if re.search(cmonth[i], prev):
                    prev = re.sub(cmonth[i], next_month[i], prev)

        # 연속 달
        # TODO ex)관리비 2,3월 수도요금 3,4월 <- 있는지 / 있으면 안됨
        #   12,1 제목 + 12 / 1 적요 => dict 처리
        if val == 1:
            # %d,%d월 확인 + %d월,%d월?
            last = int(cmonth[-1])
            first = int(cmonth[0])
            value = last - first + 1
            if last < first:
                value += 12
            next_month = month_inc(cmonth, value)
            next_month = ",".join(next_month)+"월"
            cmonth = ",".join(cmonth)+"월"
            prev = re.sub(cmonth,next_month,prev)

        # 분기 || 연단위
        if val == 2:
            # %d월~%d월 확인 + %d~%d월 ?
            last = int(cmonth[1])
            first = int(cmonth[0])
            value = last - first%12
            next_month = month_inc(cmonth,value+1)
            # nlast = int(next_month[1])
            # nfirst = int(next_month[0])
            for i in range(2):
                cmonth[i] += "월"
                next_month[i] += "월"
            # print(month,'\n',next_month)

            # if nlast < nfirst:
            #     if last > first:
            #         month.sort(reverse=True)
            #         print(month, '\n', next_month)
                # next_month.sort(reverse=True)
                # month.sort(reverse=True)
            for i in range(1,-1,-1):
                if re.search(cmonth[i], prev):
                    prev = re.sub(cmonth[i], next_month[i], prev)

    # 연도 포함 대체
    for m in cymonth:
        if val == 0:
            # %d월 확인
            next_month = ymonth_inc(cymonth, 1)
            for i in range(len(cymonth[1])):
                cymonth[1][i] += "월"
                next_month[1][i] += "월"
            cymonth[1].sort(reverse=True)
            next_month.sort(reverse=True)
            for i in range(len(cymonth[1])):
                if re.search(cymonth[0] + ' ' + cymonth[1][i], prev):
                    prev = re.sub(cymonth[0] + ' ' + cymonth[1][i], next_month[i], prev)

        # 연속 달
        # TODO ex)관리비 2,3월 수도요금 3,4월 <- 있는지 / 있으면 안됨
        #   12,1 제목 + 12 / 1 적요 => dict 처리
        if val == 1:
            # %d,%d월 확인 + %d월,%d월?
            last = int(cmonth[-1])
            first = int(cmonth[0])
            value = last - first + 1
            if last < first:
                value += 12
            next_month = month_inc(cmonth, value)
            next_month = ",".join(next_month) + "월"
            cmonth = ",".join(cmonth) + "월"
            prev = re.sub(cmonth, next_month, prev)

        # 분기 || 연단위
        if val == 2:
            # %d월~%d월 확인 + %d~%d월 ?
            last = int(cmonth[1])
            first = int(cmonth[0])
            value = last - first % 12
            next_month = month_inc(cmonth, value + 1)
            # nlast = int(next_month[1])
            # nfirst = int(next_month[0])
            for i in range(2):
                cmonth[i] += "월"
                next_month[i] += "월"
            # print(month,'\n',next_month)

            # if nlast < nfirst:
            #     if last > first:
            #         month.sort(reverse=True)
            #         print(month, '\n', next_month)
            # next_month.sort(reverse=True)
            # month.sort(reverse=True)
            for i in range(1, -1, -1):
                if re.search(cmonth[i], prev):
                    prev = re.sub(cmonth[i], next_month[i], prev)

        return prev

if __name__ == '__main__':
    sys.stdin = open("errorCase.txt")
    input()
    while True:
        put = input()
        if put[0] == "<":
            break
        print("------------------")
        print(put,"->")
        a, b, y = monthly_check(put)
        print(a,b,y)
        print(monthly_next(put, a, b, y),"<-")
        # test = input()
        # print(test)
        # print(a,b)
        # print(monthly_next(test, a, b))
        # print(a)

        break