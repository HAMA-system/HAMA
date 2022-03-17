from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time


# from openpyxl import Workbook

def fname(name, value):
    driver.find_element_by_name(name).send_keys(value)


def cname(name):
    driver.find_element_by_name(name).click()


def ename(name):
    driver.find_element_by_name(name).send_keys(Keys.ENTER)


def cpath(name):
    driver.find_element_by_path(name).click()


driver = webdriver.Chrome("/Users/MS/Downloads/chromedriver")
driver.get('https://www.hongik.ac.kr')

time.sleep(3)
cpath('/html/body/div/div[2]/ul/li[1]/a')
# driver.switch_to_window(driver.window_handles[1])
# driver.get('https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx')
# driver.get('https://cn.hongik.ac.kr')

'''
# Test Code
driver.get('https://cn.hongik.ac.kr')
result = driver.switch_to_alert()
print(result.text)
result.dismiss()
fname('USER_ID','B711020')
fname('PASSWD','test1234!@')
ename('PASSWD')
driver.send_keys("enter")
'''

# driver.switch_to.frame('/global.do')
# cpath('/html/body/div/div[2]/ul/li[1]/a')


# driver.find_element_by_name('USER_ID').send_keys('B711020')
# driver.find_element_by_name('PASSWD').send_keys('비밀번호')


test = ["2021", "2021-03-21", "2021-08-31"]
while False:
    a = input()

    if a == "조회":
        # 조회 페이지

        # 회계년도
        fname('txtAcctYear', test[0])

        # 회계구분
        select = Select(driver.find_element_by_id('ddlSAcctDivCode'))
        select.select_by_index(1)  # 비등록금 회계 테스트

        # 결의일자
        fname('DpFrDt', test[1])
        fname('DpToDt', test[2])  # 3개월 등 요소 추가 필요
        cname('CSMenuButton1$List')

    elif a == "작성":

        # 작성 페이지

        # 회계년도
        fname('txtAcctYear', test[0])

        # 결의일자
        fname('DpFrDt', test[1])
        fname('DpToDt', test[2])  # 3개월 등 요소 추가 필요
        cname('CSMenuButton1$List')

        # 엑셀 읽어들임




