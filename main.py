import sys
import os

from selenium.webdriver.common.by import By

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from FUNC_LIBRARY import autoLogin
from ESSENTIAL_FILES import manage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from EXECUTION_FILE import RUN_DRAFT

def set_chromedriver():
    options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
    options.add_argument("disable-gpu")
    try:
        # 로컬 크롬 드라이버 확인
        chrome_driver_root_path = os.path.abspath("./chromedriver")
        return webdriver.Chrome(executable_path=chrome_driver_root_path, options=options)
    except Exception as e:
        print("예외가 발생했습니다:", str(e))
        print("크롬드라이버 실행에 실패했습니다. 외부 크롬드라이버를 다운로드 합니다.")
        try:
            # 없으면 인스톨
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except Exception as e2:
            print("예외가 발생했습니다:", str(e2))
            print("외부 크롬드라이버 다운로드에 실패했습니다. 프로그램을 종료합니다.")
            raise e2

if __name__ == '__main__':
    # start = time.time()
    driver = set_chromedriver()
    driver.implicitly_wait(time_to_wait=5)
    # print(time.time()-start)
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    driver = autoLogin.login(driver)

    #### only printing option ####
    # dr = True
    dr = False

    if dr:
        while True:
            RUN_DRAFT.draft(driver)
    while True:
        # select = '조회'
        # select = '작성'
        # select = '수정'
        select = '기안'
        # select = '출근'
        if select == '조회':
            driver = autoLogin.afterLogin(driver)
            manage.lookup(driver)
        elif select == '작성':
            driver.get('https://itss.hongik.ac.kr/GateWeb/index.aspx')
            driver.execute_script("fclick(arguments[0])",
                                  driver.find_element(By.ID, "d4_AHG020P").find_element(By.TAG_NAME, "span"))
            manage.write(driver)
        elif select == '수정':
            driver = autoLogin.afterLogin(driver)
            manage.modify(driver, False)
        elif select == '기안':
            driver.get('https://itss.hongik.ac.kr/GateWeb/index.aspx')
            driver.execute_script("fclick(arguments[0])",
                                  driver.find_element(By.ID, "d4_AHG029S").find_element(By.TAG_NAME, "span"))
            RUN_DRAFT.draft_write(driver)
        elif select == '출근':
            driver = autoLogin.checkWork(driver)
        elif select == '종료':
            break
        # else:
        #     print("잘못된 입력입니다.")
