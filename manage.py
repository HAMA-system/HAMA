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
    # TODO 증빙 만들어야함
    # TODO 추가 누르면 해당탭 이동 취소 확인
    # TODO 관리코드 필요 없는 과목 있음
    # TODO 계산서 구분
    # TODO 거래처 선택 해야함

    driver.switch_to.default_content()
    autoLogin.cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/ul/li[1]/span/a')
    driver.switch_to.frame('ifr_d4_AHG020P')

    input_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('data.xlsx'),'결의내역','B3','R3')
    print(len(input_data))
    for i in range(len(input_data)):
        select = Select(driver.find_element_by_id('ddlResolutionDiv'))
        if input_data[i][1] == '수입결의서':
            select.select_by_index(0)
        elif input_data[i][1] == '지출결의서':
            select.select_by_index(1)
        autoLogin.fpath(driver,사업코드,input_data[i][0])
        time.sleep(1)
        autoLogin.epath(driver,사업코드)
        driver.switch_to.frame('frmPopup')
        time.sleep(1)
        autoLogin.epath(driver,'/html/body/form/div[3]/div[3]/ul/li/input')
        driver.switch_to.default_content()
        driver.switch_to.frame('ifr_d4_AHG020P')
        autoLogin.fpath(driver,계정과목,input_data[i][3])
        autoLogin.epath(driver,계정과목)
        autoLogin.fpath(driver,관리코드,input_data[i][4])
        autoLogin.fpath(driver,예산부서,input_data[i][7])
        autoLogin.fpath(driver,수입,input_data[i][11])
        autoLogin.fpath(driver,지출,input_data[i][12])
        autoLogin.fpath(driver,적요,input_data[i][13])
        autoLogin.cpath(driver,결의내역_제출)
        time.sleep(3)

    time.sleep(1000)