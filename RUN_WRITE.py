from selenium import webdriver
import xlsxFileController
import dateController
import errorController
import autoLogin
import manage
import sys, os, time
def set_chromedriver():
    try:
        # driver = webdriver.Chrome("./chromedriver.exe")
        # driver = webdriver.Chrome("C:/auto/chromedriver.exe")
        driver = webdriver.Chrome("/Users/han/hans/workspace/kwanjae/chromedriver")
        # driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/chromedriver")
        # driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/dist/chromedriver")

    except:
        errorController.errorMsg(0)
    return driver


driver = set_chromedriver()
driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
driver = autoLogin.login(driver)

manage.write(driver)
