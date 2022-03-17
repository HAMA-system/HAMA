from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def fname(driver,name,value):
    driver.find_element_by_name(name).send_keys(value)
def cname(driver,name):
    driver.find_element_by_name(name).click()
def ename(driver,name):
    driver.find_element_by_name(name).send_keys(Keys.ENTER)
def cpath(driver,name):
    driver.find_element_by_path(name).click()

def login(driver):

    passwd = 'jinsu781'
    passwd = passwd + input()
    fname(driver,'USER_ID','jpjung')
    fname(driver,'PASSWD',passwd)
    ename(driver,'PASSWD')
    time.sleep(2)

    # ename(driver,'PASSWD')
    result = driver.switch_to_alert()
    result.dismiss()
    # ename(driver,'PASSWD')
    # time.sleep(1)
    # alert = driver.switch_to_alert
    # alert.dismiss()
    print(1)
    # 비밀번호 변경 필요 알림 제거용


    # if EC.alert_is_present():
    #     alert = driver.switch_to_alert
    #     alert.dismiss()
    #
    # try:
    #     WebDriverWait(webbrowser, 3).until(EC.alert_is_present())
    #     alert = driver.switch_to_alert
    #     alert.dismiss()
    # except:
    #     time.sleep(1)



    return driver


if __name__ == '__main__':
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    login(driver)