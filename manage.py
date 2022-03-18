import time
import autoLogin
import dateController
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def lookup(driver):
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
    autoLogin.fpath(driver,'/html/body/form/div[5]/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div[1]/table[1]/tbody/tr[1]/td[2]/input[2]','test')