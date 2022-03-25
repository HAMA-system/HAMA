import time
import dateController
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autoLogin import *
from linkData import *
import xlsxFileController


def lookup(driver):
    driver.switch_to.default_content()
    time.sleep(1)
    cpath(driver,결의서_조회)
    driver.switch_to.frame(조회_프레임)
    while True:
        while True:
            print("원하시는 기간을 선택하세요. ex) 1/3/6/12/2022)")
            month = input().strip()
            if len(month) == 1 or len(month) == 2 or len(month) == 4:
                break
            print("잘못된 입력입니다.")

        while True:
            print("회계구분을 입력해주세요. ex) 등록금/비등록금 ")
                # acc, res = map(str,input().split())
            acc = input().strip()
            if acc == '등록금' or acc == '비등록금':
                break
            print("잘못된 입력입니다.")

        while True:
            print("결의서 구분을 입력해주세요. ex) 수입/지출/대체")
            res = input().strip()
            if res == '수입' or res == '지출' or res == '대체':
                break
            print("잘못된 입력입니다.")

        if len(month) == 4:
            fname(driver,'txtSAcctYear',month)
        else:
            fname(driver,'txtSAcctYear','2021')
        select = Select(driver.find_element_by_xpath(회계구분))
        if acc == '등록금':
            select.select_by_index(0)
        elif acc == '비등록금':
            select.select_by_index(1)

        select = Select(driver.find_element_by_xpath(결의서구분))
        if res == '수입':
            select.select_by_index(1)
        elif res == '지출':
            select.select_by_index(2)
        elif res == '대체':
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
        cname(driver,'CSMenuButton1$List')
        print("--------------------------------------------")
def write(driver):

    # TODO 증빙 만들어야함
    # TODO 추가 누르면 해당탭 이동 취소 확인
    # TODO 관리코드 필요 없는 과목 있음 if문 추가 필요
    # TODO 계산서 구분
    # TODO 거래처 선택 해야함
    # TODO 지출결의서 - 지급처
    # TODO 수입 세금계산

    driver.switch_to.default_content()
    cpath(driver,결의서_작성)
    driver.switch_to.frame(작성_프레임)

    input_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('data.xlsx'),'결의내역','B3','R3')
    # print(len(input_data))
    for i in range(len(input_data)):
        print(1)
        # time.sleep(1)
        select = Select(driver.find_element_by_id('ddlResolutionDiv'))
        print(2)
        # time.sleep(1)
        if input_data[i][1] == '수입결의서':
            select.select_by_index(0)
        elif input_data[i][1] == '지출결의서':
            select.select_by_index(1)
        print(2.5)
        # time.sleep(5) # !!!!!!!!!!
        time.sleep(3)
        fpath(driver,사업코드,input_data[i][0])
        # time.sleep(2)
        print(3)
        epath(driver,사업코드)
        print(3.5)
        # time.sleep(1) # !!!!!!!!!!
        driver.switch_to.frame('frmPopup')
        # time.sleep(1)
        print(4)
        epath(driver,사업팝업)
        driver.switch_to.default_content()
        driver.switch_to.frame('ifr_d4_AHG020P')
        fpath(driver,계정과목,input_data[i][3])
        epath(driver,계정과목)
        fpath(driver,관리코드,input_data[i][4])
        fpath(driver,예산부서,input_data[i][7])
        select = Select(driver.find_element_by_id('ddlDetailEvidenceGb'))
        input_data[i][8] = '세금'
        if input_data[i][8] == '세금':
            select.select_by_index(1)
        elif input_data[i][8] == '기타':
            select.select_by_index(2)
        elif input_data[i][8] == '영수증':
            select.select_by_index(3)

        fpath(driver,수입,input_data[i][11])
        fpath(driver,지출,input_data[i][12])
        fpath(driver,적요,input_data[i][13])
        cpath(driver,결의내역_제출)
        if input_data[i][8] == '세금':
            time.sleep(1)
            # TODO 구분 검색해서 맞는 세금 계산 찾아서 tax_data[같은 구분 줄] 해야 함. 한칸씩 미뤄야 함
            # epath(driver,결의내역_제출) # alert
            # driver.switch_to.default_content()
            driver.switch_to.alert.accept()
            tax_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('data.xlsx'), '세금계산', 'B3', 'J3')
            print(tax_data)
            fpath(driver,발행일자,tax_data[0][1].strftime("%Y%m%d"))
            epath(driver,발행일자)
            select = Select(driver.find_element_by_id('ddlBillDiv'))
            if tax_data[0][5] == '일반':
                select.select_by_index(1)
            elif tax_data[0][5] == '전자':
                select.select_by_index(2)
            elif tax_data[0][5] == '영수증':
                select.select_by_index(3)

            # TODO 거래처 고르는 것 어떡할 지 생각. tax[][2]
            fpath(driver,거래처,'')
            epath(driver,거래처)
            time.sleep(1) # 없어도 돌아가긴 함
            driver.switch_to.frame('frmPopup')

            fpath(driver,사업자번호,tax_data[0][2])
            epath(driver,사업자번호)
            driver.switch_to.default_content()
            driver.switch_to.frame('ifr_d4_AHG020P')

            # TODO 공급가액은 지출일때만 자동 (수입은 알아서 해야 함)
            cpath(driver,세금계산_제출)
            time.sleep(2)
            cpath(driver,결의내역_탭)
        time.sleep(10000)



    time.sleep(1000)

