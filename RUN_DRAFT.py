import re
import threading
import time
import os

from linkData import *
from autoLogin import *
from alertController import *
from selenium.webdriver import ActionChains

t = 0
def timeError():
    global d
    global t
    tt = 0
    while tt < 20:
        tt = t
        # print(tt)
        tt += 1
        t = tt
        time.sleep(1)
    try:
        d.window_handles[1].close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    d.get("https://ngw.hongik.ac.kr/myoffice/ezportal/index_portal.aspx")
    print("시간 초과로 재실행합니다.")
    print("오류 메시지가 뜨더라도 잠시 기다려주세요.")
    t = 0
    draft(d)

def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root
d = None
def draft(driver):

    global d
    global t
    d = driver
    te = threading.Thread(target=timeError)
    te.start()
    driver.switch_to.frame(기안_프레임1)
    cpath(driver, 결재문서)
    time.sleep(3)
    driver.switch_to.default_content()
    driver.switch_to.frame(기안_프레임2)
    cpath(driver, 완료문서)
    time.sleep(1)
    while True:
        while True:
            te.t = 0
            table = driver.find_element_by_id('DocList')
            print()
            i = 1
            for tr in table.find_elements(by=By.TAG_NAME, value="tr")[1:]:
                print("번호 ", i, " : ", sep='', end='\t')
                for td in tr.find_elements(by=By.TAG_NAME, value="td")[1:]:
                    print(td.get_attribute("innerText"), end='\t')
                print()
                i += 1
            print("\n인쇄를 할 문서들의 시작번호와 끝번호를 입력해주세요. ex) 1 20")
            print("혹은 이동할 페이지 번호를 입력해주세요. ex) 2")
            print("검색 키워드가 있는 경우 입력해주세요.")
            t = -10000
            inp = input()
            try:
                inp = list(map(int,inp.split()))
                start, end = inp[0], inp[1]
                break
            except:
                t = 10
                try:
                    inp = int(inp[0])
                    page = 페이지_변경[:29] + str(inp + 2) + 페이지_변경[30:]
                    cpath(driver, page)
                    time.sleep(1)
                except:
                    driver.find_element_by_id("txt_keyword").clear()
                    driver.find_element_by_id("txt_keyword").send_keys(inp)
                    driver.find_element_by_id("txt_keyword").send_keys(Keys.ENTER)
                    # fpath(driver, 기안_검색, inp[0])
                    # epath(driver, 기안_검색)
                    time.sleep(2)
        # if len(inp) == 2:
        #     start, end = inp[0], inp[1]
        # elif len(inp) == 1:
        #     page = 페이지_변경[:29] + str(inp[0]+2) + 페이지_변경[30:]
        #     cpath(driver, page)
        #     time.sleep(1)
        #     continue
        for i in range(start, end+1):
            # 시작할 때, 반복할 때 주소가 달라야 클릭이 됨
            t = 5
            if i == start:
                num = 문서번호1[:64] + str(i) + 문서번호1[65:]
            else:
                num = 문서번호2[:67] + str(i) + 문서번호2[68:]
            print(i,"번 문서 인쇄중...",sep='')
            cpath(driver, num)
            time.sleep(3)
            cpath(driver, 인쇄)
            time.sleep(1)
            driver.switch_to.frame(메인_프레임)
            cpath(driver, 문서인쇄)
            t = 0
            while True:
                try:
                    driver.switch_to.window(driver.window_handles[1])
                    break
                except:
                    time.sleep(2)
            t = 5
            d = driver
            # time.sleep(20)

            # ** shadow-root 같은 element는 find_element(by=) 이용해야함 **
            # driver.switch_to.window(driver.window_handles[1])
            r0 = driver.find_element(by=By.CSS_SELECTOR, value=섀도0)
            sr0 = expand_shadow_element(driver, r0)
            r1 = sr0.find_element(by=By.CSS_SELECTOR,value=섀도1)
            sr1 = expand_shadow_element(driver, r1)
            r2 = sr1.find_element(by=By.CSS_SELECTOR,value=섀도2)
            sr2 = expand_shadow_element(driver, r2)
            save = sr2.find_element(by=By.CLASS_NAME,value=인쇄확인)
            save.click()
            time.sleep(1)

            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.default_content()
            driver.switch_to.frame(기안_프레임2)
            driver.switch_to.frame(메인_프레임)
            cpath(driver, 인쇄_창닫기)
            driver.switch_to.parent_frame()
            cpath(driver, 기안_창닫기)

        print("모든 문서 출력이 완료되었습니다.")
def draft_write(driver):

    # TODO
    #   굳이 엔터 누르지 않아도 가능하나
    #   엔터 받지 않으면 자동으로 window[0]으로 가야함

    cpath(driver,결의서_조회)

    while True:
        print("\n변경하실 페이지를 띄우신 후 엔터를 눌러주세요")
        input()
        try:
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        try:
            driver.switch_to.alert.dismiss()
        except:
            pass
        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)
        driver.switch_to.frame('frmPopup')
        cid(driver, 기안)
        last = len(driver.window_handles)
        while True:
            try:
                driver.switch_to.window(driver.window_handles[last])
                break
            except:
                pass
        driver.switch_to.frame('message')
        table = driver.find_element(by=By.ID, value='ctlTable')
        i = 1
        title = driver.find_element(by=By.XPATH, value=기안_제목).get_attribute("innerText")
        for tr in table.find_elements(by=By.TAG_NAME, value="tr")[6:]:
            for td in tr.find_elements(by=By.TAG_NAME, value="td")[2:]:
                money = td.get_attribute("innerText")
            i += 1
        money = int("".join(money.split(",")))
        결재 = 부총결
        기록물 = 위탁
        if re.match('.지출결의서.',title):
            기록물 = 용역
            if money >= 300000:
                결재 = 총결
        driver.switch_to.default_content()
        cid(driver, 결재정보)
        driver.switch_to.frame(메인_프레임)
        cid(driver, 즐겨찾기)
        cid(driver, 결재)
        cpath(driver, 적용)
        cid(driver, 기록물철)
        cid(driver, 기록물)
        cpath(driver, 기안_확인)

        # draft_uproad(driver)
        print("결재정보 입력이 완료되었습니다.")
        # time.sleep(1)
        # while True:
        #     try:
        #         driver.switch_to.window(driver.window_handles[0])
        #         break
        #     except:
        #         pass
        # cid(driver, 기안_종료)
        # print("기안이 완료되었습니다.")

def draft_uproad(driver):
    # path = 링크[3] + str(num) + '/'
    # exist = 0
    # for x in os.listdir(링크[3]):
    #     if x == str(num):
    #         exist = 1
    #         break
    # if exist:
    #     cpath(driver, 첨부파일)
    #     driver.switch_to.window(driver.window_handles[1])
    #     for f in os.listdir(path):
    #         driver.find_element_by_xpath(파일선택).send_keys(path + f)
    #         time.sleep(0.3)
    #         cpath(driver, 파일업로드)
    #         print(f, "파일 업로드 완료")
    try:
        driver.switch_to.frame(driver.window_handles[0])
    except:
        print(0)
    driver.switch_to.default_content()
    print(1)
    cid(driver, 'btnFileAttach')
    print(2)
    path = 링크[3] + 'test' + '/'
    for f in os.listdir(path):
        driver.find_element(by=By.ID, value='imgbtn').send_keys(path + f)
        time.sleep(0.3)
    time.sleep(1)
    cpath(driver, '/html/body/div/div[2]/ul/li/a/span')
    print("파일 첨부 완료")
    time.sleep(100)

# TODO
#   결재정보 -> 즐겨찾기 -> 결제 -> 적용 -> 기록물철 -> 지급/징수 -> 확인 -> 닫기
#   수입 - 부총장님 + 위탁
#   지출 - 30만원 이상) 총장님 + 용역 / 30만원 미만) 부총장님 + 용역


'''

1. 엑셀 파일 토대로 폴더 생성 (중복 확인) 
2. 폴더 이름과 파일 이름 매칭하여 옮기기
3. 파일 업로드할 때 앞에 번호만 확인


정기 아닌경우 -> 키워드에 파일 이름에 들어가는 고유한 키워드 적어달라 하기

파일 남아있을 때 메세지

'''
