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
        driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/chromedriver")
        # driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/dist/chromedriver")

    except:
        errorController.errorMsg(0)
    return driver

if __name__ == '__main__':
    # if getattr(sys, 'frozen', False):
    #     chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver")
    #     driver = webdriver.Chrome(chromedriver_path)
    # else:
    #     driver = webdriver.Chrome()


    driver = set_chromedriver()
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    driver = autoLogin.login(driver)
    while True:
        # print("원하시는 서비스를 입력하세요. (조회/작성/종료)")
        # select = input()
        select = '작성'
        if select == '조회':
            manage.lookup(driver)
        elif select == '작성':
            manage.write(driver)
        elif select == '종료':
            break
        else:
            print("잘못된 입력입니다.")
