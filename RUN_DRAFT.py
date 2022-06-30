import re
import threading
import time
import os

import manage
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
    # try:
    #     d.window_handles[1].close()
    #     d.switch_to.window(d.window_handles[0])
    # except:
    #     pass
    # d.get("https://ngw.hongik.ac.kr/myoffice/ezportal/index_portal.aspx")
    # print("시간 초과로 재실행합니다.")
    # print("오류 메시지가 뜨더라도 잠시 기다려주세요.")
    # t = 0
    # draft(d)

def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root
d = None

# TODO
#   - Print
#       흑백 처리
#       멈추면 오류나는거 다시 고쳐야함
#   - Replace
#       따로 파일 옮기는 프로그램 생성
#
def draft(driver):

    global d
    global t

    d = driver
    te = threading.Thread(target=timeError)
    te.daemon = True
    te.start()
    driver.switch_to.default_content()
    driver.switch_to.frame(기안_프레임1)
    cpath(driver, 결재문서)
    time.sleep(3)
    driver.switch_to.default_content()
    driver.switch_to.frame(기안_프레임2)
    cpath(driver, 완료문서)
    time.sleep(1)
    first = True
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
                    time.sleep(2)
        for i in range(start, end+1):
            # 시작할 때, 반복할 때 주소가 달라야 클릭이 됨
            t = 5
            # if i == start:
            if first:
                num = 문서번호1[:64] + str(i) + 문서번호1[65:]
                first = False
            else:
                num = 문서번호2[:67] + str(i) + 문서번호2[68:]
            print(i,"번 문서 인쇄중...",sep='')
            cpath(driver, num)
            time.sleep(3)
            cpath(driver, 인쇄)
            time.sleep(1)
            driver.switch_to.frame(메인_프레임)
            cpath(driver, 문서인쇄)
            t = -5
            time.sleep(5)
            while True:
                if t >= 20:
                    # print("TEST")
                    t = 0
                    driver.get("https://ngw.hongik.ac.kr/myoffice/ezportal/index_portal.aspx")
                    return
                try:
                    driver.switch_to.window(driver.window_handles[1])
                    break
                except:
                    # print("no window")
                    time.sleep(3)
            t = 5
            # d = driver

            # ** shadow-root 같은 element는 find_element(by=) 이용해야함 **
            # driver.switch_to.window(driver.window_handles[1])
            r0 = driver.find_element(by=By.CSS_SELECTOR, value=섀도0)
            sr0 = expand_shadow_element(driver, r0)
            r1 = sr0.find_element(by=By.CSS_SELECTOR,value=섀도1)
            sr1 = expand_shadow_element(driver, r1)

            # Color Setting
            sc0 = sr1.find_element(by=By.CSS_SELECTOR,value=섀도컬0)
            scr0 = expand_shadow_element(driver, sc0)
            sc1 = scr0.find_element(by=By.CSS_SELECTOR,value=섀도컬1)
            src1 = expand_shadow_element(driver,sc1)

            color = Select(driver.find_element(by=By.XPATH, value=컬러세팅))
            color.select_by_index(0)

            # Print
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

    cpath(driver,결의서_조회)
    first = True
    while True:
        if not first:
            print("\n기안이 완료되면 엔터를 눌러주세요")
            input()
        first = False
        try:
            driver.find_element(by=By.XPATH, value=기안_종료)
        except:
            pass
        try:
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(조회_프레임)
            driver.find_element(by=By.XPATH, value=닫기)
        except:
            pass
        try:
            driver.switch_to.alert.dismiss()
        except:
            pass
        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)
        manage.search(driver)

        print("\n변경하실 페이지를 띄우신 후 엔터를 눌러주세요")
        print("다시 검색을 원하시면 1을 입력해주세요")
        put = input()
        if put == '1':
            first = True
            continue
        # try:
        #     driver.switch_to.window(driver.window_handles[0])
        # except:
        #     pass
        # try:
        #     driver.switch_to.alert.dismiss()
        # except:
        #     pass
        # driver.switch_to.default_content()
        # driver.switch_to.frame(조회_프레임)
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
        # print(title)
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


        # driver.switch_to.default_content()
        # time.sleep(0.4)
        # cid(driver, 기안_종료)
        # driver.switch_to.window(driver.window_handles[0])
        # driver.switch_to.default_content()
        # driver.switch_to.frame(조회_프레임)
        # cpath(driver, 닫기)


        # draft_uproad(driver, title)
        # print("결재정보 입력이 완료되었습니다.")
        # time.sleep(1)
        # while True:
        #     try:
        #         driver.switch_to.window(driver.window_handles[0])
        #         break
        #     except:
        #         pass
        # cid(driver, 기안_종료)
        # print("기안이 완료되었습니다.")

def draft_uproad(driver, title):

    driver.switch_to.default_content()
    cid(driver, 기안_파일버튼)
    time.sleep(0.5)
    path = 링크[3] + 'out/'
    driver.switch_to.frame(메인_프레임)
    driver.switch_to.frame('dadiframe')
    for x in os.listdir(path):
        if re.search("".join(x.split()[1:]), title):
            xpath = path + x + "/"
            for y in os.listdir(xpath):
                driver.find_element_by_xpath(기안_파일).send_keys(xpath + y)
                print(y,"업로드 완료")
            break
    time.sleep(1)
    print("파일 첨부 완료")
    driver.switch_to.parent_frame()
    print("\n결재를 올리시겠습니까? 1(예)")
    print("만약 파일이 잘못된 경우 올바른 파일을 업로드 후 1을 입력해주세요")
    while True:
        put = input()
        if put == '1':
            cpath(driver,기안_업로드)
            driver.switch_to.default_content()
            time.sleep(0.2)
            cid(driver,결재올림)
            driver.switch_to.frame(메인_프레임)
            time.sleep(0.2)
            cid(driver,결재확인)
            driver.switch_to.default_content()
            time.sleep(0.4)
            cid(driver,기안_종료)
            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.default_content()
            driver.switch_to.frame(조회_프레임)
            cpath(driver,닫기)
            break
        else:
            print("잘못된 입력입니다.")
    # cpath(driver, '/html/body/div/div[2]/ul/li/a/span')
    # driver.switch_to.default_content()
    # time.sleep(100)

    # TODO
    #   같은 파일이 여럿 있을 때
    #   - 대학로캠퍼스 신한은행 연간임대료
    #       - 2022-03-31_신한은행연납.pdf
    #   - 서울캠(신한은행) 임대료
    #       - 신한은행 2022년 입금.pdf
    #       - 신한은행 2022년 위탁료.pdf
    #   - 대학로캠퍼스 신한은행 관리비(2월) 입금
    #       - 2022-03-07 신한은행.pdf
    #   - 서울캠(신한은행) 관리비2월분)
    #       - 신한은행 입금 1.pdf
    #       - 신한은행 입금 2.pdf
    #       - 신한은행 2월.pdf

    # TODO
    #   방법 생각
    #   - 폴더 이름을 결의서 제목으로?
    #       -> 파일은 키워드로 찾아 넣기
    #       문제점 : 별도의 추가 프로세스 필요, 편리한가
    #   -
    #   별도
    #   - 작성 필요 폴더, 기안 필요 폴더, 완료 폴더 생성하면 편리하실지
    #   복사
    #   복사점
    #   복사점 3월.pdf
