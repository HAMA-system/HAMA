from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import loginData
import time

def fname(driver,name,value):
    # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, name)))
    time.sleep(0.3)
    driver.find_element_by_name(name).clear()
    # element.clear()
    time.sleep(0.3)
    driver.find_element_by_name(name).send_keys(value)
    # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, name)))
    # element.send_keys(value)
def cname(driver,name):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, name)))
    element.click()
def ename(driver,name):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, name)))
    element.send_keys(Keys.ENTER)
def fpath(driver,path,value):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    element.send_keys(value)
def cpath(driver,path):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    element.click()

def login(driver):
    fname(driver,'USER_ID',loginData.ID)
    fname(driver,'PASSWD',loginData.PW)
    ename(driver,'PASSWD')
    # driver.get('https://itss.hongik.ac.kr/GateWeb/index.aspx')
    print("확인 후 아무 키나 입력해주세요")
    a = input()
    driver.get('https://itss.hongik.ac.kr/GateWeb/index.aspx')
    # time.sleep(1)
    cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/a')
    # time.sleep(0.3)
    cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/a')
    # time.sleep(0.3)
    cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/a')
    # time.sleep(0.3)
    cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/a')
    return driver
    # time.sleep(0.3)
    # cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/ul/li[2]/span/a')
    # ename(driver,'PASSWD')

    # ename(driver,'PASSWD')
    # time.sleep(1)
    # alert = driver.switch_to_alert
    # alert.dismiss()
    # print(1)
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



    # return driver


if __name__ == '__main__':
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    login(driver)