from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from linkData import *
import loginData
import time
import xlsxFileController

def fname(driver,name,value):
    # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, name)))
    time.sleep(0.1)
    driver.find_element_by_name(name).clear()
    # element.clear()
    time.sleep(0.2)
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
    # time.sleep(0.35) # 0.5
    while True:
        try:
            driver.find_element_by_xpath(path).clear()
            break
        except:
            pass
    # time.sleep(0.25) # 0.4
    while True:
        try:
            driver.find_element_by_xpath(path).send_keys(value)
            break
        except:
            pass
    # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    # element.clear()
    # time.sleep(1)
    # element.send_keys(value)
def cpath(driver,path):
    # time.sleep(0.5)
    while True:
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
            break
        except:
            pass
    while True:
        try:
            element.click()
            break
        except:
            pass
def cpathDouble(driver,path):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    element.click()
    element.click()

def epath(driver,path):
    time.sleep(0.2)
    driver.find_element_by_xpath(path).send_keys(Keys.ENTER)
    # element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
    # element.send_keys(Keys.ENTER)

def login(driver):
    login_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('loginData.xlsx'), '로그인', 'B60', 'C60')
    # login_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('C:/auto/loginData.xlsx'), '로그인', 'B60', 'C60')

    fname(driver,'USER_ID',login_data[0])
    fname(driver,'PASSWD',login_data[1])
    ename(driver,'PASSWD')
    # time.sleep(1)
    try:
        driver.switch_to.alert.accept()
    except:
        pass

    return afterLogin(driver)
    # return checkWork(driver)

def afterLogin(driver):
    driver.get('https://itss.hongik.ac.kr/GateWeb/index.aspx')
    cpath(driver, '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/a')
    cpath(driver, '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/a')
    cpath(driver, '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/a')
    cpath(driver, '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/a')
    return driver


def checkWork(driver):
    driver.get('https://hrm.hongik.ac.kr/new/')
    # cpath(driver, 출근버튼)
    # cpath(driver, 출근버튼a)
    # cpath(driver, 출근버튼b)


if __name__ == '__main__':
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    login(driver)