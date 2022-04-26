import os
import time

import autoLogin
import dateController
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from autoLogin import *
from linkData import *
from alertController import *
import xlsxFileController
import ignoreAutoLogout
import threading
from sys import stdout

sema = 0
d = ''
def refresh():
    # TODO
    #   작성에서도 되게 바꿔야 함.
    cpath(d,조회)

def printProgress(i, max):
    c = int(i*max)
    stdout.write('\r[' + '#'*c + ' '*(max-c-1) + ']\t\t[' + str(int(i*100)) + '%]')

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
        time.sleep(0.5)
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
            print("회계 구분번호를 입력해주세요. ex) 1(등록금)/2(비등록금)/3(종료) ")
            acc = input().strip()
            if acc == '1' or acc == '2' or acc == '3':
                break
            print("잘못된 입력입니다.")
        if acc == '3':
            break
        while True:
            sema = 1
            print("결의서 구분번호를 입력해주세요. ex) 1(전체)/2(수입)/3(지출)/4(대체)")
            res = input().strip()
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
            # 정기 체크
            print(-2)
            if target_data[i][0] != -1 or prev != -1:
                w = 1
                if prev != target_data[i][0]:
                    if tax == 1:
                        print(prev, isMonthly, row)
                        file = taxWrite(driver, prev, file, isMonthly, row)
                        tax = 0
                    row = 15 + i
                    isMonthly = False

                    save(driver)
                    if target_data[i][0] == -1:
                        prev = target_data[i][0]
                        continue
                    acceptAlert(driver)

                    upload(driver, prev)
                    cpath(driver,신규)
                    for p in range(len(target_data)):
                        if target_data[p][0] == prev:
                            xlsxFileController.put_cell_data(file, '결의내역', 'E'+str(p+15), -1)
                    time.sleep(0.5)

                    print("구분번호 :", target_data[i][0])

                print(i + 15, '행 입력중입니다.', sep='')
                if target_data[i][1] is not None and target_data[i][1] != '':
                    isMonthly = True
                    print(-1.5)
                    target_data[i][18] = str(target_data[i][18])
                    print(-1.4)
                    for j in range(len(target_data[i][18])):
                        if target_data[i][18][j] == '월':
                            print(str(target_data[i][18][j-1]), str(target_data[i][2]))
                            target_data[i][18] = target_data[i][18].replace(str(target_data[i][18][j-1]), str(target_data[i][2]))
                    if target_data[i][3] is not None and target_data[i][3] != '':
                        target_data[i][3] = str(target_data[i][3])
                        for j in range(len(target_data[i][3])):
                            if target_data[i][3][j] == '월':
                                print(str(target_data[i][3][j-1]), str(target_data[i][2]))
                                target_data[i][3] = target_data[i][3].replace(str(target_data[i][3][j-1]), str(target_data[i][2]))

                    print("*******************",target_data[i][18])
                    print("*******************",target_data[i][3])

                    print(-1.3)
                    print(target_data[i][18])
                    print(-1)
                # stdout.flush()
                # printProgress(progress/progrexx_max, progress_size)
                # progress += progress/progrexx_max
                print(-0.5)
                time.sleep(0.5)
                for j in range(len(target_data[i])):
                    print(j, target_data[i][j])
                if target_data[i][4] is not None and target_data[i][4] != '':
                    target_data[i][4] = str(target_data[i][4])[:10]
                    # if target_data[i][2][:4] != '2022':
                    #     time.sleep(1)
                    #     fpath(driver, 회계년도, target_data[i][2][:2])
                    #     fpath(driver, 'txtSAcctYear', target_data[i][2][:4])
                    #     time.sleep(5000)
                    #     time.sleep(0.2)
                print(-0.3)
                select = Select(driver.find_element_by_xpath(회계구분_작성))
                print(-0.25)
                if target_data[i][5] is not None and target_data[i][5] != '':
                    if target_data[i][5] == '등록금':
                        select.select_by_index(0)
                    elif target_data[i][5] == '비등록금' or target_data[i][5] == '(서울)기숙사':
                        select.select_by_index(1)
                    time.sleep(0.2)

                if target_data[i][4] is not None and target_data[i][4] != '':
                    fpath(driver,결의일자_번호,target_data[i][4])
                print(-0.2)
                select = Select(driver.find_element_by_id('ddlResolutionDiv'))
                if target_data[i][6] is not None and target_data[i][6] != '':
                    test3 = {"수입" : 0, "지출" : 1, "대체" : 2}
                    select.select_by_index(test3[target_data[i][6]])

                    fpath(driver,사업코드,target_data[i][5])
                    epath(driver,사업코드)
                    driver.switch_to.frame('frmPopup')
                    epath(driver,사업팝업)
                    driver.switch_to.default_content()
                    driver.switch_to.frame('ifr_d4_AHG020P')
                print(0)
                if target_data[i][3] is not None and target_data[i][3] != '':
                    fpath(driver,결의서_제목,target_data[i][3])
                fpath(driver,계정과목,target_data[i][8])
                epath(driver,계정과목)

                if target_data[i][9] is not None and target_data[i][9] != '':
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
                print(1)
                if target_data[i][11] is not None and target_data[i][11] != '':
                    if target_data[i][11] == '기숙사':
                        dorm(driver, 귀속부서, 귀속부서팝업)
                    else:
                        fpath(driver, 귀속부서, target_data[i][11])
                        epath(driver, 귀속부서)

                if target_data[i][12] is not None and target_data[i][12] != '':
                    if target_data[i][12] == '기숙사':
                        dorm(driver, 예산부서, 예산부서팝업)
                    else:
                        fpath(driver, 예산부서, target_data[i][12])
                        epath(driver, 예산부서)
                print(2)
                select = Select(driver.find_element_by_id('ddlDetailEvidenceGb'))
                print(2.3)
                test2 = {"없음" : 0, "세금" : 1, "기타" : 2, "현금" : 3}
                select.select_by_index(test2[target_data[i][13]])

                if target_data[i][16] is not None and target_data[i][16] != '':
                    fpath(driver,지출,target_data[i][16])
                if target_data[i][17] is not None and target_data[i][17] != '':
                    fpath(driver,수입,target_data[i][17])
                if target_data[i][18] is not None and target_data[i][18] != '':
                    fpath(driver,적요,target_data[i][18])
                print(2.5)
                time.sleep(0.2)
                cpath(driver,결의내역_제출)
                time.sleep(0.3)

                if target_data[i][13] == '세금':
                    tax = 1
                    dismissAlert(driver)

            prev = target_data[i][0]
            print(3)
            if i == len(target_data)-1 and w == 1:
                print(4)
                if tax == 1:
                    file = taxWrite(driver, target_data[i][0], file, isMonthly, row)
                    tax = 0

                save(driver)
                upload(driver, prev)

                for p in range(len(target_data)):
                    if target_data[p][0] == prev:
                        xlsxFileController.put_cell_data(file, '결의내역', 'E' + str(p+15), -1)
                print("입력이 완료되었습니다.")
                xlsxFileController.save_xls(file)
        # delete(file)

    except:
        print('오류가 발생하여 초기화면으로 돌아갑니다')
        # driver.refresh()
        autoLogin.afterLogin(driver)
        xlsxFileController.save_xls(file)

def taxWrite(driver, num, file, isMonthly, row):
    time.sleep(0.3)
    cpath(driver, 세금계산_탭)
    print(num, isMonthly, row)
    if isMonthly:
        tax_data = xlsxFileController.all_data_fetch(file, '결의내역', 'AB'+str(row), 'AJ'+str(row))
    else:
        tax_data = xlsxFileController.all_data_fetch(file, '세금계산', 'E20', 'L20')
    print("T1")
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

            if tax_data[j][4] is not None and tax_data[j][4] != '':
                fpath(driver, 공급가액, tax_data[j][4])
                fpath(driver, 세액, tax_data[j][5])

            select = Select(driver.find_element_by_id('ddlBillDiv'))
            test1 = {"일반" : 1, "전자" : 2, "현금" : 3}
            select.select_by_index(test1[tax_data[j][6]])
            cpath(driver, 세금계산_제출)
            time.sleep(0.5)

    for p in range(len(tax_data)):
        if tax_data[p][0] == num:
            if isMonthly:
                xlsxFileController.put_cell_data(file, '결의내역', 'AB' + str(p+row), -1)
            else:
                xlsxFileController.put_cell_data(file, '세금계산', 'E' + str(p+20), -1)
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
        # sv = input()
        sv = '1'
        if sv == '1':
            break
        else:
            time.sleep(3)

    cpath(driver,저장)
    time.sleep(0.3)

def delete(file):
    print("입력된 데이터를 전부 삭제하겠습니까? 1(예)/2(아니오)")
    d = input().strip()
    if d == '1':
        xlsxFileController.delete_completed_row(file, '결의내역', 'E', 'Y', 15)
        xlsxFileController.delete_completed_row(file, '세금계산', 'E', 'L', 20)
        xlsxFileController.save_xls(file)
        print("삭제가 완료되었습니다.")
