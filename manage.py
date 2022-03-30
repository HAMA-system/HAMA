import time
import dateController
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autoLogin import *
from linkData import *
import xlsxFileController
import ignoreAutoLogout
import threading
sema = 0
d = ''
def refresh():
    # TODO
    #   작성에서도 되게 바꿔야 함.
    cpath(d,조회)

def lookup(driver):
    global sema
    global d
    d = driver
    ig = threading.Thread(target=ignoreAutoLogout.startTimer)
    ig.daemon = True
    ig.start()

    driver.switch_to.default_content()
    time.sleep(1)
    cpath(driver,결의서_조회)
    driver.switch_to.frame(조회_프레임)
    while True:
        while True:
            ignoreAutoLogout.timer = 0
            sema = 0
            print("회계 구분번호를 입력해주세요. ex) 1(등록금)/2(비등록금)/3(뒤로가기) ")
                # acc, res = map(str,input().split())
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
        # if search is not None:
        fpath(driver,제목_검색,search)
        cname(driver,'CSMenuButton1$List')
        print("--------------------------------------------")
def write(driver):

    # TODO
    #   지급처 추가
    #   해결할 것 :
    #   미지급금 관리코드 오류 처리
    #   거래처 코드 11 처럼 두자리면 클릭해야함
    #   한국후지필름 11, 8687 등등 있는데 아무거나 해도 되는지 (엑셀엔 8687, 결의서 내역엔 11)

    global sema
    global d
    d = driver

    driver.switch_to.default_content()
    cpath(driver,결의서_작성)
    driver.switch_to.frame(작성_프레임)
    file = xlsxFileController.load_xls('data.xlsx')
    input_data = xlsxFileController.all_data_fetch(file,'결의내역','E3','V3')
    # for x in input_data:
    #     if x[0] == -1:
    #         del x
    # print(len(input_data))
    # TODO
    prev = input_data[0][0]
    tax = 0
    for i in range(len(input_data)):
        if input_data[i][0] != '-1':
            # TODO
            if prev != input_data[i][0]:
                if tax == 1:
                    tax = taxWrite(driver, prev)
                cpath(driver,저장)
                time.sleep(2)
                try:
                    driver.switch_to.alert.accept()
                except:
                    pass
                cpath(driver,신규)
                for p in range (len(input_data)):
                    if input_data[p][0] == prev:
                        print('E'+str(p+3))
                        xlsxFileController.put_cell_data(file, '결의내역', 'E'+str(p+3), '-1')
                xlsxFileController.save_xls(file)

                time.sleep(0.5)
            print(i + 3, '행 입력중입니다.', sep='')
            select = Select(driver.find_element_by_xpath(회계구분_작성))
            if input_data[i][3] is not None:
                if input_data[i][3] == '등록금':
                    select.select_by_index(0)
                elif input_data[i][3] == '비등록금':
                    select.select_by_index(1)
                time.sleep(0.3)
            if input_data[i][2] is not None:
                fpath(driver,결의일자_번호,input_data[i][2])

            # print(1)
            # time.sleep(1)
            select = Select(driver.find_element_by_id('ddlResolutionDiv'))
            # print(2)
            # time.sleep(1)
            if input_data[i][4] is not None:
                if input_data[i][4] == '수입결의서':
                    select.select_by_index(0)
                elif input_data[i][4] == '지출결의서':
                    select.select_by_index(1)
                time.sleep(1)
                fpath(driver,사업코드,input_data[i][3])
                epath(driver,사업코드)
                driver.switch_to.frame('frmPopup')
                epath(driver,사업팝업)
                driver.switch_to.default_content()
                driver.switch_to.frame('ifr_d4_AHG020P')

            if input_data[i][1] is not None:
                fpath(driver,결의서_제목,input_data[i][1])
            fpath(driver,계정과목,input_data[i][6])
            epath(driver,계정과목)
            if input_data[i][7] is not None:
                fpath(driver,관리코드,input_data[i][7])
                epath(driver,관리코드)

                try:
                    driver.switch_to.alert.accept()
                except:
                    driver.switch_to.frame('frmPopup')
                    epath(driver,관리팝업)
                    driver.switch_to.default_content()
                    driver.switch_to.frame('ifr_d4_AHG020P')
            fpath(driver,예산부서,input_data[i][9])
            select = Select(driver.find_element_by_id('ddlDetailEvidenceGb'))

            if input_data[i][11] == '없음':
                select.select_by_index(0)
            elif input_data[i][11] == '세금':
                select.select_by_index(1)
            elif input_data[i][11] == '기타':
                select.select_by_index(2)
            elif input_data[i][11] == '영수증':
                select.select_by_index(3)

            if input_data[i][14] is not None:
                fpath(driver,지출,input_data[i][14])
            if input_data[i][15] is not None:
                fpath(driver,수입,input_data[i][15])
            if input_data[i][16] is not None:
                fpath(driver,적요,input_data[i][16])
            cpath(driver,결의내역_제출)

            if input_data[i][11] == '세금':
                time.sleep(0.3)
                tax = 1
                try:
                    driver.switch_to.alert.dismiss()
                except:
                    pass
            prev = input_data[i][0]

        if i == len(input_data)-1:
            if tax == 1:
                tax = taxWrite(driver, input_data[i][0])
            cpath(driver,저장)
            for p in range(len(input_data)):
                if input_data[p][0] == prev:
                    print('E' + str(p + 3))
                    xlsxFileController.put_cell_data(file, '결의내역', 'E' + str(p + 3), '-1')
            xlsxFileController.save_xls(file)
            time.sleep(1)
            try:
                driver.switch_to.alert.dismiss()
            except:
                pass
            print("입력이 완료되었습니다.")

def taxWrite(driver, num):
    time.sleep(0.3)
    cpath(driver, 세금계산_탭)
    tax_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('data.xlsx'), '세금계산', 'E3', 'L3')

    for j in range(len(tax_data)):
        if tax_data[j][0] == num:

            select = Select(driver.find_element_by_xpath(과세구분))
            # TODO 선택지 추가 필요 !!
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

            # TODO elif 추가
            fpath(driver, 발행일자, tax_data[j][2].strftime("%Y%m%d"))
            epath(driver, 발행일자)
            # TODO 거래처 고르는 것 어떡할 지 생각. tax[][2]
            fpath(driver, 거래처, '')
            epath(driver, 거래처)
            time.sleep(0.5)  # 없어도 돌아가긴 함

            driver.switch_to.frame('frmPopup')

            fpath(driver, 사업자번호, tax_data[j][3])
            epath(driver, 사업자번호)
            driver.switch_to.default_content()
            driver.switch_to.frame('ifr_d4_AHG020P')

            if tax_data[j][4] is not None:
                fpath(driver, 공급가액, tax_data[j][4])
                fpath(driver, 세액, str(int(tax_data[j][4] / 10)))

            select = Select(driver.find_element_by_id('ddlBillDiv'))
            if tax_data[j][6] == '일반':
                select.select_by_index(1)
            elif tax_data[j][6] == '전자':
                select.select_by_index(2)
            elif tax_data[j][6] == '영수증':
                select.select_by_index(3)

            cpath(driver, 세금계산_제출)
            time.sleep(0.5)
    cpath(driver, 결의내역_탭)
    print("세금처리가 완료되었습니다.")
    return 0
