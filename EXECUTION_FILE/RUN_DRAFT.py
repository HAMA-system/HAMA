import re
import threading
import os
import time

from ESSENTIAL_FILES import manage
from FUNC_LIBRARY.autoLogin import *
from selenium.webdriver.support.ui import Select

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
            if first:
                num = 문서번호1[:64] + str(i) + 문서번호1[65:]
                first = False
            else:
                num = 문서번호2[:67] + str(i) + 문서번호2[68:]
            print(i,"번 문서 인쇄중...",sep='')
            cpath(driver, num)
            time.sleep(3)
            try:
                cid(driver, 'tabAttachInfoDT')
                pdf_num = 1
                print_path = 'C:/Users/admin/Downloads/'
                while True:
                    try:
                        pdf_link = '/html/body/div[3]/div[1]/div/span[2]/span[2]/span/span/div[1]/div[3]/div/div[1]/ul/li/ul/ul/li/a['+str(pdf_num)+']/ul/li/span'
                        pdf_down = driver.find_element(by=By.XPATH, value=pdf_link)
                        pdf_down.click()
                        pdf_num += 1
                        t = 0
                        Max = 0
                        last_file = ''
                        # 가장 최근에 추가된 파일로 이용.
                        # 이름 추출하여 비교하는 게 시간 더 오래 걸림
                        for file in os.listdir(print_path):
                            written_time = os.path.getctime(print_path + file)
                            if Max < written_time:
                                Max = written_time
                                last_file = file
                            os.startfile(print_path + file, 'print')
                            time.sleep(1)
                    except:
                        break
            except:
                pass
            # 다운로드 폴더에서 pdf 파일 이름 비교 후 프린트
            # os.startfile("test", "print")

            # 어디 경로로 들어가는지
            # 기본 인쇄 옵션 어떻게 되는지
            # 엑셀 어떻게 되는지
            # 가장 최근 문서 vs 이름 찾기

            # test = driver.find_element(by=By.XPATH,
            #                            value='/html/body/div[3]/div[1]/div/span[2]/span[2]/span/span/div[1]/div[3]/div/div[1]/ul/li/ul')
            # for li in test.find_elements(by=By.TAG_NAME, value="li")[1:]:
            #     print(li.get_attribute("innerText"))

            cpath(driver, 인쇄)
            time.sleep(1)
            driver.switch_to.frame(메인_프레임)
            cpath(driver, 문서인쇄)
            t = -5
            time.sleep(5)
            while True:
                if t >= 20:
                    t = 0
                    driver.get("https://ngw.hongik.ac.kr/myoffice/ezportal/index_portal.aspx")
                    return
                try:
                    driver.switch_to.window(driver.window_handles[1])
                    break
                except:
                    time.sleep(3)
            t = 5
            # ** shadow-root 같은 element는 find_element(by=) 이용해야함 **
            # driver.switch_to.window(driver.window_handles[1])
            r0 = driver.find_element(by=By.CSS_SELECTOR, value=섀도0)
            sr0 = expand_shadow_element(driver, r0)
            r1 = sr0.find_element(by=By.CSS_SELECTOR,value=섀도1)
            sr1 = expand_shadow_element(driver, r1)

            # Color Setting
            sc0 = sr1.find_element(by=By.CSS_SELECTOR,value=섀도컬0)
            scr0 = expand_shadow_element(driver, sc0)
            # sc1 = scr0.find_element(by=By.CSS_SELECTOR,value=섀도컬1)
            # scr1 = expand_shadow_element(driver, sc1)

            color = Select(scr0.find_element(by=By.CLASS_NAME, value=컬러세팅))
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
        # Alert 오류 제어
        try:
            driver.switch_to.alert.dismiss()
        except:
            pass

        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)

        # 처음에만 검색
        if first:
            manage.search(driver)
            first = False

        while True:
            print("\n변경하실 페이지를 띄우신 후 원하시는 버튼을 입력해주세요.")
            print("1(다음달로 복사 후 기안) 2(바로 기안)")

            put = input()
            if put == '1':
                manage.modify(driver, True)

                # Alert 오류 제어
                try:
                    driver.switch_to.alert.dismiss()
                except:
                    pass
                break
            elif put == '2':
                driver.switch_to.frame('frmPopup')
                break
            else:
                print("잘못된 입력입니다.")

        cid(driver, 기안)
        try:
            driver.switch_to.alert.dismiss()
            print("업로드된 파일이 없습니다.\n파일 업로드 후 엔터를 눌러주세요")
            input()
            manage.save(driver)
            cid(driver, 기안)

        except:
            pass

        # 기안 창으로 이동
        while True:
            try:
                driver.switch_to.window(driver.window_handles[1])
                break
            except:
                pass
        driver.switch_to.frame('message')

        # 테이블에서 기안 제목 및 금액 받아옴
        table = driver.find_element(by=By.ID, value='ctlTable')
        i = 1
        title = driver.find_element(by=By.XPATH, value=기안_제목).get_attribute("innerText")
        for tr in table.find_elements(by=By.TAG_NAME, value="tr")[6:]:
            for td in tr.find_elements(by=By.TAG_NAME, value="td")[2:]:
                money = td.get_attribute("innerText")
            i += 1
        money = int("".join(money.split(",")))

        # 결재정보 저장
        결재 = 부총결
        기록물 = 위탁
        if re.match('.지출결의서.',title):
            기록물 = 용역
            if money >= 300000:
                결재 = 총결

        # 결재
        driver.switch_to.default_content()
        cid(driver, 결재정보)
        driver.switch_to.frame(메인_프레임)
        cid(driver, 즐겨찾기)
        cid(driver, 결재)
        cpath(driver, 적용)
        cid(driver, 기록물철)
        cid(driver, 기록물)
        cpath(driver, 기안_확인)

        # 기안 업로드
        draft_upload(driver, title, True)
        # draft_upload(driver, title, False)

        # driver.switch_to.default_content()
        # cid(driver, 기안_파일버튼)
        # print("기안이 완료되면 엔터를 눌러주세요")
        # input()

        # 기안 창 닫기
        # driver.switch_to.default_content()
        # driver.find_element(by=By.ID, value=기안_종료).click()
        # time.sleep(0.5)
        # driver.switch_to.frame(메인_프레임)
        # driver.find_element(by=By.ID, value=결재확인).click()
        # driver.switch_to.window(driver.window_handles[0])
        # driver.switch_to.default_content()
        # driver.switch_to.frame(조회_프레임)
        # driver.find_element(by=By.XPATH, value=닫기).click()


def draft_upload(driver, title, isFile):

    uploaded = True

    driver.switch_to.default_content()
    cid(driver, 기안_파일버튼)
    time.sleep(0.5)
    path = 링크[3] + '기안 필요/'
    driver.switch_to.frame(메인_프레임)
    driver.switch_to.frame('dadiframe')
    for folder in os.listdir(path):
        searchKey = "".join(folder.split('#')[:-1]).replace('$','/').replace("(","\(").replace(")","\)").strip()
        if re.search(searchKey, title.strip()):
            draftFolder = path + folder + "/"
            for file in os.listdir(draftFolder):
                driver.find_element_by_xpath(기안_파일).send_keys(draftFolder + file)

                # 로딩 안되고 올라가면 스킵되는 듯?
                time.sleep(1.5)
                print(file,"업로드 완료")
            if '완료' not in os.listdir(링크[3]):
                os.mkdir(링크[3] + '완료')
            os.replace(draftFolder, 링크[3] + "완료/" + folder)
            break
    else:
        print("기안 필요 폴더에 알맞은 폴더가 없습니다\n파일 업로드 후 결재올림을 눌러주세요.")
        uploaded = False

    if uploaded:
        # time.sleep(1)
        # driver.switch_to.parent_frame()
        print("파일 첨부가 완료되었습니다. 결재올림을 눌러주세요.")
        # print("\n결재를 올리시겠습니까? 1(예)")
        # print("만약 파일이 잘못된 경우 올바른 파일을 업로드 후 1을 입력해주세요")

        # while True:
        #     put = input()
        #     if put == '1':
        #         cpath(driver,기안_업로드)
        #         driver.switch_to.default_content()
        #         time.sleep(0.2)
        #         cid(driver,결재올림)
        #         driver.switch_to.frame(메인_프레임)
        #         time.sleep(0.2)
        #         cid(driver,결재확인)
        #         break
        #     else:
        #         print("잘못된 입력입니다.")

    while True:
        try:
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
        except:
            driver.switch_to.window(driver.window_handles[0])
            break
    # driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.default_content()
    driver.switch_to.frame(조회_프레임)
    cpath(driver, 닫기)

