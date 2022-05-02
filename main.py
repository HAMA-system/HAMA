import autoLogin
import manage
import time
from selenium import webdriver
from linkData import *
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
def set_chromedriver():
    while True:
        try:
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            # driver = webdriver.Chrome(executable_path=링크[0])
            break
            # driver = webdriver.Chrome("/Users/han/hans/workspace/kwanjae/chromedriver")
            # driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/chromedriver")

        except:
            pass
            # errorController.errorMsg(0)
    return driver

if __name__ == '__main__':
    start = time.time()
    driver = set_chromedriver()
    driver.implicitly_wait(time_to_wait=10)
    print(time.time()-start)
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    driver = autoLogin.login(driver)
    while True:
        # select = '조회'
        # select = '작성'
        select = '수정'
        if select == '조회':
            manage.lookup(driver)
        elif select == '작성':
            manage.write(driver)
        elif select == '수정':
            manage.modify(driver)
        # elif select == '종료':
        #     break
        # else:
        #     print("잘못된 입력입니다.")
