from selenium import webdriver
import xlsxFileController
import dateController
import errorController
import autoLogin
import manage
import manageRefactoring
import sys, os, time
from linkData import *
def set_chromedriver():
    try:
        driver = webdriver.Chrome(링크[0])
        # driver = webdriver.Chrome("/Users/han/hans/workspace/kwanjae/chromedriver")
        # driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/chromedriver")

    except:
        errorController.errorMsg(0)
    return driver

if __name__ == '__main__':
    # path = "/Users/MS/PycharmProjects/HAMA/1"
    # uploadFile = path + '/'
    # for x in os.listdir(path):
    #     uploadFile += x + '\n'
    # print(uploadFile)
    # time.sleep(10000)
    driver = set_chromedriver()
    driver.implicitly_wait(time_to_wait=10)
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    driver = autoLogin.login(driver)
    while True:
        # select = '조회'
        select = '작성'
        if select == '조회':
            manage.lookup(driver)
        elif select == '작성':
            manageRefactoring.write(driver)
        # elif select == '종료':
        #     break
        # else:
        #     print("잘못된 입력입니다.")
