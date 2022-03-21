from selenium import webdriver
import xlsxFileController
import dateController
import errorController
import autoLogin
import manage


def set_chromedriver():
    try:
        driver = webdriver.Chrome("./chromedriver")
    except:
        errorController.errorMsg(0)
    return driver

if __name__ == '__main__':
    driver = set_chromedriver()
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    driver = autoLogin.login(driver)
    while True:
        print("원하시는 서비스를 입력하세요. (조회/작성/종료)")
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
