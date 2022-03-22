import time
import autoLogin
import dateController
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import xlsxFileController


def lookup(driver):
    driver.switch_to.default_content()
    time.sleep(1)
    autoLogin.cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/ul/li[2]/span/a')
    driver.switch_to.frame('ifr_d4_AHG029S')
    while True:
        print("원하시는 기간을 선택하세요.(1/3/6/12/종료)")
        month = input()
        autoLogin.fname(driver,'txtSAcctYear','2021')
        if month == '1':
            autoLogin.fname(driver,'DpFrDt',dateController.date1month())
        elif month == '3':
            autoLogin.fname(driver,'DpFrDt',dateController.date3month())
        elif month == '6':
            autoLogin.fname(driver,'DpFrDt',dateController.date6month())
        elif month == '12':
            autoLogin.fname(driver,'DpFrDt',dateController.date1year())
        # elif month == '학기':
        #     autoLogin.fname(driver,'DpFrDt') # DpToDt 고쳐야 함

        elif month == '종료':
            break
        else:
            print("잘못된 입력입니다.")
        autoLogin.fname(driver,'DpToDt',dateController.dateToday())
        autoLogin.cname(driver,'CSMenuButton1$List')
def write(driver):
    계정과목 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[1]/td[2]/input[2]'
    관리코드 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[2]/td[1]/input[2]'
    예산부서 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[2]/td[3]/input[2]'
    수입 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[4]/td[1]/input'
    지출 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[4]/td[2]/input'
    적요 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[4]/td[3]/input'
    결의내역_제출 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/div[3]/ul/li[7]/span/input[2]'
    세금계산_탭 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[1]/td/div/table/tbody/tr/td[4]'
    사업코드 = '/html/body/form/div[3]/div[3]/div[1]/table/tbody/tr[3]/td[1]/input[2]'
    지급예정일 = '/html/body/form/div[3]/div[3]/div[1]/table/tbody/tr[3]/td[2]/input'
    발행일자 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[3]/table[1]/tbody/tr[1]/td[2]/input'
    거래처 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[3]/table[1]/tbody/tr[1]/td[3]/table/tbody/tr/td[1]/input[4]'
    세금계산_제출 = '/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[3]/table[2]/tbody/tr/td/div/span[3]/input[2]'

    # TODO 증빙 만들어야함
    # TODO 추가 누르면 해당탭 이동 취소 확인
    # TODO 관리코드 필요 없는 과목 있음
    # TODO 계산서 구분
    # TODO 거래처 선택 해야함

    driver.switch_to.default_content()
    autoLogin.cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/ul/li[1]/span/a')
    driver.switch_to.frame('ifr_d4_AHG020P')

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
        autoLogin.fpath(driver,사업코드,input_data[i][0])
        # time.sleep(2)
        print(3)
        autoLogin.epath(driver,사업코드)
        print(3.5)
        # time.sleep(1) # !!!!!!!!!!
        driver.switch_to.frame('frmPopup')
        # time.sleep(1)
        print(4)
        autoLogin.epath(driver,'/html/body/form/div[3]/div[3]/ul/li/input')
        driver.switch_to.default_content()
        driver.switch_to.frame('ifr_d4_AHG020P')
        autoLogin.fpath(driver,계정과목,input_data[i][3])
        autoLogin.epath(driver,계정과목)
        autoLogin.fpath(driver,관리코드,input_data[i][4])
        autoLogin.fpath(driver,예산부서,input_data[i][7])
        select = Select(driver.find_element_by_id('ddlDetailEvidenceGb'))
        input_data[i][8] = '세금'
        if input_data[i][8] == '세금':
            select.select_by_index(1)
        elif input_data[i][8] == '기타':
            select.select_by_index(2)
        elif input_data[i][8] == '영수증':
            select.select_by_index(3)

        autoLogin.fpath(driver,수입,input_data[i][11])
        autoLogin.fpath(driver,지출,input_data[i][12])
        autoLogin.fpath(driver,적요,input_data[i][13])
        autoLogin.cpath(driver,결의내역_제출)
        if input_data[i][8] == '세금':
            time.sleep(1)
            # TODO 구분 검색해서 맞는 세금 계산 찾아서 tax_data[같은 구분 줄] 해야 함. 한칸씩 미뤄야 함
            # autoLogin.epath(driver,결의내역_제출) # alert
            # driver.switch_to.default_content()
            driver.switch_to.alert.accept()
            tax_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('data.xlsx'), '세금계산', 'B3', 'J3')
            print(tax_data)
            autoLogin.fpath(driver,발행일자,tax_data[0][1].strftime("%Y%m%d"))
            autoLogin.epath(driver,발행일자)
            select = Select(driver.find_element_by_id('ddlBillDiv'))
            if tax_data[0][5] == '일반':
                select.select_by_index(1)
            elif tax_data[0][5] == '전자':
                select.select_by_index(2)
            elif tax_data[0][5] == '영수증':
                select.select_by_index(3)

            # TODO 거래처 고르는 것 어떡할 지 생각. tax[][2]
            autoLogin.fpath(driver,거래처,'미니스톱')
            autoLogin.epath(driver,거래처)
            time.sleep(1) # 없어도 돌아가긴 함

            autoLogin.cpath(driver,세금계산_제출)
        time.sleep(1000)



    time.sleep(1000)