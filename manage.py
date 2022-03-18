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
    time.sleep(3)
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
    driver.switch_to.default_content()
    autoLogin.cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/ul/li[1]/span/a')
    driver.switch_to.frame('ifr_d4_AHG020P')
    select = Select(driver.find_element_by_id('ddlResolutionDiv'))
    input_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('data.xlsx'),'결의내역','B3','R3')
    print(input_data)
    input_data[0][0]
    if input_data[0][1] == '수입결의서':
        select.select_by_index(0)
    elif input_data[0][1] == '지출결의서':
        select.select_by_index(1)

    autoLogin.fpath(driver,'/html/body/form/div[3]/div[3]/div[1]/table/tbody/tr[3]/td[1]/input[2]',input_data[0][0])
    autoLogin.epath(driver,'/html/body/form/div[3]/div[3]/div[1]/table/tbody/tr[3]/td[1]/input[2]')

    driver.switch_to.frame('frmPopup')
    autoLogin.epath(driver,'/html/body/form/div[3]/div[3]/ul/li/input')

    time.sleep(0.5)
    print(1)
    driver.switch_to.default_content()
    driver.switch_to.frame('ifr_d4_AHG020P')
    # autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[1]/td[2]/input[2]',input_data[0])
    # autoLogin.epath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[1]/td[2]/input[2]')


    # 세금계산 탭 이동
    #autoLogin.cpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[1]/td/div/table/tbody/tr/td[4]')

    # 계정과목
    autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[1]/td[3]/input[2]',input_data[0][3])
    autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[2]/td[1]/input[2]',input_data[0][4])
    autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[2]/td[3]/input[2]',input_data[0][7])

    #증빙 만들어야함
    autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[4]/td[1]/input',input_data[0][11])
    autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[4]/td[2]/input',input_data[0][12])
    autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[4]/td[3]/input',input_data[0][13])
    autoLogin.cpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/div[3]/ul/li[7]/span/input[2]')
    # autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[2]/td[1]/input[2]',input_data[2])
    # autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[2]/td[3]/input[2]',input_data[3])