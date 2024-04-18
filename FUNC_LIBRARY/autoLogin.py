from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from HIDDEN_FILES.linkData import *
import time
from . import xlsxFileController


def fillByName(driver, name, value):
    time.sleep(0.1)
    driver.find_element_by_name(name).clear()
    time.sleep(0.2)
    driver.find_element_by_name(name).send_keys(value)


def clickByName(driver, name):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, name)))
    element.click()


def enterByName(driver, name):
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, name)))
    element.send_keys(Keys.ENTER)


def fillByXPath(driver, path, value):
    time.sleep(0.1)
    while True:
        try:
            driver.find_element_by_xpath(path).clear()
            break
        except:
            pass
    time.sleep(0.2)
    while True:
        try:
            driver.find_element_by_xpath(path).send_keys(value)
            break
        except:
            pass


def clickByXPath(driver, path):
    time.sleep(0.1)
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


def enterByXPath(driver, path):
    time.sleep(0.2)
    while True:
        try:
            driver.find_element_by_xpath(path).send_keys(Keys.ENTER)
            break
        except:
            pass


def fillById(driver, id, value):
    time.sleep(0.1)
    while True:
        try:
            driver.find_element_by_id(id).clear()
            break
        except:
            pass
    time.sleep(0.2)
    while True:
        try:
            driver.find_element_by_id(id).send_keys(value)
            break
        except:
            pass


def clickById(driver, id):
    time.sleep(0.1)
    while True:
        try:
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, id)))
            break
        except:
            pass
    while True:
        try:
            element.click()
            break
        except:
            pass


def login(driver):
    login_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls(링크[1]), '로그인', 'B60', 'C60')

    fillByName(driver, 'USER_ID', login_data[0])
    fillByName(driver, 'PASSWD', login_data[1])
    enterByName(driver, 'PASSWD')
    time.sleep(1)
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    return driver
    # return afterLogin(driver)
    # return checkWork(driver)


def afterLogin(driver):
    driver.get('https://itss.hongik.ac.kr/GateWeb/index.aspx')
    clickByXPath(driver, '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/a')
    clickByXPath(driver, '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/a')
    clickByXPath(driver, '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/a')
    clickByXPath(driver, '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/a')
    checkUpdatePasswordAlert(driver)
    return driver


def checkWork(driver):
    driver.get('https://hrm.hongik.ac.kr/new/')
    clickByXPath(driver, 출근버튼)
    time.sleep(10000)

def checkUpdatePasswordAlert(driver):
    try:
        driver.switch_to.alert.accept()
    except:
        pass

if __name__ == '__main__':
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    login(driver)