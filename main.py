import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from FUNC_LIBRARY import autoLogin
from ESSENTIAL_FILES import manage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from EXECUTION_FILE import RUN_DRAFT


def set_chromedriver():
    while True:
        try:
            options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
            # options.add_argument('headless')  # headless 모드 설정
            # options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
            options.add_argument("disable-gpu")
            # options.add_argument("disable-infobars")
            # options.add_argument("--disable-extensions")

            # prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
            #                                                     'geolocation': 2, 'notifications': 2,
            #                                                     'auto_select_certificate': 2, 'fullscreen': 2,
            #                                                     'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
            #                                                     'media_stream_mic': 2, 'media_stream_camera': 2,
            #                                                     'protocol_handlers': 2, 'ppapi_broker': 2,
            #                                                     'automatic_downloads': 2, 'midi_sysex': 2,
            #                                                     'push_messaging': 2, 'ssl_cert_decisions': 2,
            #                                                     'metro_switch_to_desktop': 2,
            #                                                     'protected_media_identifier': 2, 'app_banner': 2,
            #                                                     'site_engagement': 2, 'durable_storage': 2}}
            # options.add_experimental_option('prefs', prefs)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            # driver = webdriver.Chrome(executable_path=링크[0],options=options)

            # driver = webdriver.Chrome(링크[0])

            break
            # driver = webdriver.Chrome("/Users/han/hans/workspace/kwanjae/chromedriver")
            # driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/chromedriver")

        except:
            pass
            # errorController.errorMsg(0)
    return driver

if __name__ == '__main__':
    # start = time.time()
    driver = set_chromedriver()
    driver.implicitly_wait(time_to_wait=10)
    # print(time.time()-start)
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    driver = autoLogin.login(driver)
    # dr = True
    dr = False
    if dr:
        while True:
            RUN_DRAFT.draft(driver)
    else:
        driver = autoLogin.afterLogin(driver)
    while True:
        # select = '조회'
        # select = '작성'
        # select = '수정'
        select = '기안'
        if select == '조회':
            manage.lookup(driver)
        elif select == '작성':
            # rep = threading.Thread(target=RUN_REPLACE.replace())
            # rep.start()
            manage.write(driver)
        elif select == '수정':
            manage.modify(driver, False)
        elif select == '기안':
            RUN_DRAFT.draft_write(driver)
        elif select == '종료':
            break
        # else:
        #     print("잘못된 입력입니다.")
