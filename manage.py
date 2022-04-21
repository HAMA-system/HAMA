import os
import time

import autoLogin
import dateController
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from autoLogin import *
from linkData import *
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
    #   지급처 추가
    #   해결할 것 :
    #   미지급금 관리코드 오류 처리
    #   거래처 코드 11 처럼 두자리면 클릭해야함
    #   한국후지필름 11, 8687 등등 있는데 아무거나 해도 되는지 (엑셀엔 8687, 결의서 내역엔 11)
    #   세금처리에서 문제 생기면 세금계산 시트 -1 안되도록
    #   저장 빼놓기
    #   렉 걸릴때 처리할 것 추가
    #   추가 할 것 :
    #   i 유지 코드
    #   가서 여러줄 받고 돌아오게 하기
    #

    # TODO
    #   input_data[i][17] > 0, isMonthly = 1
    #   isMonthly == 1, change sheet -> while input_data[j][0] != input_data[i][17] j++ (+ tax)
    #   if end, return i
    #   Solutions?
    #       - use queue?
    #           > for i in range -> while queue
    #           > tax_write(driver, tax_queue)
    #           > queue[0][0] = row num
    #           > while queue[0][1] == input_data[row num][1], queue popleft
    #       -
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
        input_data = xlsxFileController.all_data_fetch(file,'결의내역','E15','W15')
        # monthly_data = xlsxFileController.all_data_fetch(file,'결의내역(정기)','E15','W15')
        w = 0
        prev = input_data[0][0]
        tax = 0

        target_data = input_data
        isMonthly = False

        if input_data[0][0] != -1:
            print("구분번호 :",input_data[0][0])
        for i in range(len(input_data)):
            # 정기체크 후 정기면 target_data = monthly_data
            # 아니면 target_data = input_data

            # if input_data[i][17] > 0:
            #     # temp = i
            #     # i = input_data[i][17]
            #     target_data = monthly_data
            #     isMonthly = True
            # else:
            #     target_data = input_data
            #     isMonthly = False

            if target_data[i][0] != -1 or prev != -1:
                w = 1
                if prev != target_data[i][0]:
                    if tax == 1:
                        file = taxWrite(driver, prev, file)
                        tax = 0

                    # while True:
                    #     print("저장하시겠습니까? 1(예)/ 2(아니오)")
                    #     save = input()
                    #     if save == '1':
                    #         break
                    #     else:
                    #         time.sleep(3)

                    cpath(driver,저장)
                    time.sleep(0.3)

                    if target_data[i][0] == -1:
                        prev = target_data[i][0]
                        continue

                    while True:
                        try:
                            driver.switch_to.alert.accept()
                            break
                        except:
                            pass

                    upload(driver, prev)
                    cpath(driver,신규)

                    print("구분번호 :", target_data[i][0])
                    for p in range(len(target_data)):
                        if target_data[p][0] == prev:
                            xlsxFileController.put_cell_data(file, '결의내역', 'E'+str(p+15), -1)

                    time.sleep(0.5)
                print(i + 15, '행 입력중입니다.', sep='')
                # stdout.flush()
                # printProgress(progress/progrexx_max, progress_size)
                # progress += progress/progrexx_max

                time.sleep(0.5)

                if target_data[i][2] is not None:
                    target_data[i][2] = str(target_data[i][2])[:10]
                #     if target_data[i][2][:4] != '2022':
                #         time.sleep(1)
                #         fpath(driver, 회계년도, target_data[i][2][:2])
                #         time.sleep(5)
                #         time.sleep(0.2)

                select = Select(driver.find_element_by_xpath(회계구분_작성))
                if target_data[i][3] is not None:
                    if target_data[i][3] == '등록금':
                        select.select_by_index(0)
                    elif target_data[i][3] == '비등록금' or target_data[i][3] == '(서울)기숙사':
                        select.select_by_index(1)
                    time.sleep(0.2)

                if target_data[i][2] is not None:
                    fpath(driver,결의일자_번호,target_data[i][2])

                select = Select(driver.find_element_by_id('ddlResolutionDiv'))
                if target_data[i][4] is not None:
                    if target_data[i][4] == '수입':
                        select.select_by_index(0)
                    elif target_data[i][4] == '지출':
                        select.select_by_index(1)
                    elif target_data[i][4] == '대체':
                        select.select_by_index(2)
                    fpath(driver,사업코드,target_data[i][3])
                    epath(driver,사업코드)
                    driver.switch_to.frame('frmPopup')
                    epath(driver,사업팝업)
                    driver.switch_to.default_content()
                    driver.switch_to.frame('ifr_d4_AHG020P')

                if target_data[i][1] is not None:
                    fpath(driver,결의서_제목,target_data[i][1])
                fpath(driver,계정과목,target_data[i][6])
                epath(driver,계정과목)

                if target_data[i][7] is not None:
                    fpath(driver,관리코드,target_data[i][7])
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

                if target_data[i][9] is not None:
                    if target_data[i][9] == '기숙사':
                        dorm(driver, 귀속부서, 귀속부서팝업)
                    else:
                        fpath(driver, 귀속부서, target_data[i][9])
                        epath(driver, 귀속부서)

                if target_data[i][10] is not None:
                    if target_data[i][10] == '기숙사':
                        dorm(driver, 예산부서, 예산부서팝업)
                    else:
                        fpath(driver, 예산부서, target_data[i][10])
                        epath(driver, 예산부서)

                select = Select(driver.find_element_by_id('ddlDetailEvidenceGb'))
                if target_data[i][11] == '없음':
                    select.select_by_index(0)
                elif target_data[i][11] == '세금':
                    select.select_by_index(1)
                elif target_data[i][11] == '기타':
                    select.select_by_index(2)
                elif target_data[i][11] == '현금':
                    select.select_by_index(3)

                if target_data[i][14] is not None:
                    fpath(driver,지출,target_data[i][14])
                if target_data[i][15] is not None:
                    fpath(driver,수입,target_data[i][15])
                if target_data[i][16] is not None:
                    fpath(driver,적요,target_data[i][16])
                cpath(driver,결의내역_제출)
                time.sleep(0.3)

                if target_data[i][11] == '세금':
                    tax = 1
                    while True:
                        try:
                            driver.switch_to.alert.dismiss()
                            break
                        except:
                            pass
            prev = target_data[i][0]

            if i == len(target_data)-1 and w == 1:
                if tax == 1:
                    file = taxWrite(driver, target_data[i][0], file, isMonthly)
                    tax = 0
                # while True:
                #     print("저장하시겠습니까? 1(예)/2(아니오)")
                #     save = input()
                #     if save == '1':
                #         break
                #     else:
                #         time.sleep(3)

                cpath(driver,저장)
                time.sleep(0.3)
                while True:
                    try:
                        driver.switch_to.alert.dismiss()
                        break
                    except:
                        pass
                upload(driver, prev)

                for p in range(len(target_data)):
                    if target_data[p][0] == prev:
                        xlsxFileController.put_cell_data(file, '결의내역', 'E' + str(p+15), -1)
                print("입력이 완료되었습니다.")
                xlsxFileController.save_xls(file)

        # print("입력된 데이터를 전부 삭제하겠습니까? 1(예)/2(아니오)")
        # d = input().strip()
        # if d == '1':
        #     xlsxFileController.delete_completed_row(file, '결의내역', 'E', 'Y', 15)
        #     xlsxFileController.delete_completed_row(file, '세금계산', 'E', 'L', 20)
        #     xlsxFileController.save_xls(file)
        #     print("삭제가 완료되었습니다.")

    except:
        print('오류가 발생하여 초기화면으로 돌아갑니다')
        driver.refresh()
        autoLogin.afterLogin(driver)
        xlsxFileController.save_xls(file)

def taxWrite(driver, num, file, isMonthly):
    time.sleep(0.3)
    cpath(driver, 세금계산_탭)
    if isMonthly:
        tax_data = xlsxFileController.all_data_fetch(file, '세금계산(정기)', 'E20', 'L20')
    else:
        tax_data = xlsxFileController.all_data_fetch(file, '세금계산', 'E20', 'L20')
    for j in range(len(tax_data)):
        if tax_data[j][0] == num:
            select = Select(driver.find_element_by_xpath(과세구분))
            if tax_data[j][1] == '매입세금-불':
                select.select_by_index(1)
            elif tax_data[j][1] == '매입세금':
                select.select_by_index(2)
            elif tax_data[j][1] == '매입계산':
                select.select_by_index(3)
            elif tax_data[j][1] == '매출세금':
                select.select_by_index(4)
            elif tax_data[j][1] == '매출계산':
                select.select_by_index(5)
            elif tax_data[j][1] == '매출세금-불':
                select.select_by_index(6)
            elif tax_data[j][1] == '수입세금':
                select.select_by_index(7)
            elif tax_data[j][1] == '수입계산':
                select.select_by_index(8)
            elif tax_data[j][1] == '매입세금-간':
                select.select_by_index(9)

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

            if tax_data[j][4] is not None:
                fpath(driver, 공급가액, tax_data[j][4])
                fpath(driver, 세액, tax_data[j][5])

            select = Select(driver.find_element_by_id('ddlBillDiv'))
            if tax_data[j][6] == '일반':
                select.select_by_index(1)
            elif tax_data[j][6] == '전자':
                select.select_by_index(2)
            elif tax_data[j][6] == '현금':
                select.select_by_index(3)
            cpath(driver, 세금계산_제출)
            time.sleep(0.5)
    for p in range(len(tax_data)):
        if tax_data[p][0] == num:
            xlsxFileController.put_cell_data(file, '세금계산', 'E' + str(p+20), -1)
    cpath(driver, 결의내역_탭)
    print("세금처리가 완료되었습니다.")
    return file

def upload(driver, num):
    path = 링크[3] + str(num) + '/'
    exist = 0
    for x in 링크[3]:
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
        while True:
            try:
                driver.switch_to.alert.dismiss()
                break
            except:
                pass