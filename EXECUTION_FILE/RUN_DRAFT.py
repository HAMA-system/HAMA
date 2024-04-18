import re
import subprocess
import threading
import os
import time

from ESSENTIAL_FILES import manage
from FUNC_LIBRARY.autoLogin import *
from FUNC_LIBRARY import ignoreAutoLogout
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


def refresh():
    clickByXPath(d, 조회)


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", element)
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
    clickByXPath(driver, 결재문서)
    time.sleep(3)
    driver.switch_to.default_content()
    driver.switch_to.frame(기안_프레임2)
    driver.find_element_by_id('LOCKMYCONT').click()
    time.sleep(1)
    first = True
    while True:
        while True:
            te.t = 0
            table = driver.find_element_by_id("DocList")
            print()
            i = 1
            for tr in table.find_elements(by=By.TAG_NAME, value="tr")[1:]:
                print("번호 ", i, " : ", sep="", end="\t")
                for td in tr.find_elements(by=By.TAG_NAME, value="td")[1:]:
                    print(td.get_attribute("innerText"), end="\t")
                print()
                i += 1
            print("\n인쇄를 할 문서들의 시작번호와 끝번호를 입력해주세요. ex) 1 20")
            print("혹은 이동할 페이지 번호를 입력해주세요. ex) 2")
            print("검색 키워드가 있는 경우 입력해주세요.")
            t = -10000
            inp = input()
            try:
                inp = list(map(int, inp.split()))
                start, end = inp[0], inp[1]
                break
            except:
                t = 10
                try:
                    inp = int(inp[0])
                    page = 페이지_변경[:29] + str(inp + 2) + 페이지_변경[30:]
                    clickByXPath(driver, page)
                    time.sleep(1)
                except:
                    driver.find_element_by_id("txt_keyword").clear()
                    driver.find_element_by_id("txt_keyword").send_keys(inp)
                    driver.find_element_by_id("txt_keyword").send_keys(Keys.ENTER)
                    time.sleep(2)
        for i in range(start, end + 1):
            # 시작할 때, 반복할 때 주소가 달라야 클릭이 됨
            t = 5
            if first:
                num = 문서번호1[:64] + str(i) + 문서번호1[65:]
                first = False
            else:
                num = 문서번호2[:67] + str(i) + 문서번호2[68:]
            print(i, "번 문서 인쇄중...", sep="")

            clickByXPath(driver, num)
            time.sleep(3)

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

            clickByXPath(driver, 인쇄)
            time.sleep(1)
            driver.switch_to.frame(메인_프레임)
            clickByXPath(driver, 문서인쇄)
            t = -5
            time.sleep(5)
            while True:
                if t >= 20:
                    t = 0
                    driver.get(
                        "https://ngw.hongik.ac.kr/myoffice/ezportal/index_portal.aspx"
                    )
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
            r1 = sr0.find_element(by=By.CSS_SELECTOR, value=섀도1)
            sr1 = expand_shadow_element(driver, r1)

            # Color Setting
            sc0 = sr1.find_element(by=By.CSS_SELECTOR, value=섀도컬0)
            scr0 = expand_shadow_element(driver, sc0)

            sc1 = scr0.find_element(by=By.CSS_SELECTOR, value=섀도컬1)
            scr1 = expand_shadow_element(driver, sc1)

            # color = Select(scr0.find_element(by=By.CLASS_NAME, value=컬러세팅))

            try:
                color = Select(scr1.find_element(by=By.CSS_SELECTOR, value="md-select"))
                color.select_by_index(0)
            except:
                print("컬러 설정 생략")
                pass

            # Print
            r2 = sr1.find_element(by=By.CSS_SELECTOR, value=섀도2)
            sr2 = expand_shadow_element(driver, r2)
            save = sr2.find_element(by=By.CLASS_NAME, value=인쇄확인)
            save.click()
            time.sleep(1)

            driver.switch_to.window(driver.window_handles[0])
            driver.switch_to.default_content()
            driver.switch_to.frame(기안_프레임2)
            driver.switch_to.frame(메인_프레임)
            clickByXPath(driver, 인쇄_창닫기)
            driver.switch_to.parent_frame()

            # # 첨부파일 프린트
            # try:
            #     print("첨부 파일 다운로드를 시작합니다")
            #     clickById(driver, "tabAttachInfoDT")
            #     pdf_num = 1
            #     print_path = download_path
            #     while True:
            #         try:
            #             pdf_link = (
            #                 "/html/body/div[3]/div[1]/div/span[2]/span[2]/span/span/div[1]/div[3]/div/div[1]/ul/li/ul/ul/li/a["
            #                 + str(pdf_num)
            #                 + "]/ul/li/span"
            #             )
            #             pdf_down = driver.find_element(by=By.XPATH, value=pdf_link)
            #             pdf_down.click()
            #             pdf_num += 1
            #             t = 0
            #             Max = 0
            #             last_file = ""
            #             # 가장 최근에 추가된 파일로 이용.
            #             # 이름 추출하여 비교하는 게 시간 더 오래 걸림
            #             time.sleep(1.5)
            #             for file in os.listdir(print_path):
            #                 if file[0] == ".":
            #                     continue
            #                 written_time = os.path.getctime(print_path + file)
            #                 if Max < written_time:
            #                     Max = written_time
            #                     last_file = file
            #             print(print_path + last_file, "파일이 프린트되고 있습니다...")
            #             os.startfile(print_path + last_file, "print")
            #         except:
            #             print("첨부파일 출력 완료")
            #             break
            # except:
            #     pass

            driver.switch_to.default_content()
            driver.switch_to.frame(기안_프레임2)
            try:
                close_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.ID, "embed_Close"))
                )
                close_btn.click()
            except:
                input("창 닫기에 실패하였습니다. 수동으로 종료 후 [Enter]를 눌러주세요")
                pass

            print(i, "번 문서 출력 완료", sep="")

        print("모든 문서 출력이 완료되었습니다.")


def draft_write(driver):
    global d
    d = driver
    ig = threading.Thread(target=ignoreAutoLogout.startTimer)
    ig.daemon = True
    ignoreAutoLogout.timer = 0
    ig.start()
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

        # 기안 메뉴 loop
        no_file = False  # 파일 오류 여부 체크
        month_change_completed = False # 특정 월로 복사 후 기안완료인지 체크
        while True:
            # 선택지 loop
            while True:
                print("\n변경하실 페이지를 띄우신 후 원하시는 버튼을 입력해주세요.")
                put = input("1(다음달로 복사 후 기안) 2(바로 기안) 3(검색으로 돌아가기) 4(특정 월로 복사 후 기안) 5(다음달로 복사 후 미지급금 기안)\n")
                if put == "1": # 다음달로 복사 후 기안
                    manage.modify(driver, True)

                    # Alert 오류 제어
                    try:
                        driver.switch_to.alert.dismiss()
                    except:
                        pass
                    break
                elif put == "2": # 바로 기안
                    try:
                        print("로드 중입니다. 최대 30초 소요될 수 있습니다.")
                        if no_file == False:
                            driver.switch_to.frame("frmPopup")
                        no_file = True
                    except:
                        print("잘못된 입력입니다. 다시 시도해주세요")
                    break
                elif put == "3": # 검색으로 돌아가기
                    first = True
                    break
                elif put == "4": # 특정 월로 복사 후 기안
                    while True:
                        month = input("변경하고자 하려는 월을 입력하세요\n")
                        try:
                            int_month = int(month)
                        except:
                            print("잘못된 입력입니다. 다시 시도해주세요")
                            continue
                        if 1 <= int_month <= 12:
                            manage.modify_month(driver, int_month)
                            month_change_completed = True
                            break
                        print("잘못된 입력입니다. 다시 시도해주세요")
                    # Alert 오류 제어
                    try:
                        driver.switch_to.alert.dismiss()
                    except:
                        pass
                    if month_change_completed == True:
                        continue
                    break

                # if put == "5": # 다음달로 복사 후 미지급금 기안
                #     manage.modify_non_paid(driver, True)
                #     # Alert 오류 제어
                #     try:
                #         driver.switch_to.alert.dismiss()
                #     except:
                #         pass
                #     break

                else:
                    print("잘못된 입력입니다.")
            # 검색으로 돌아가기
            if first == True:
                break
            # 선택지 loop end

            try:
                clickById(driver, 기안)
            except:
                print("기안할 수 없습니다. 다시 확인하고 시도해주세요.")
                break

            # 파일 업로드 실패 처리
            try:
                driver.switch_to.alert.dismiss()
                print("업로드된 파일이 없습니다. 다시 시도해주세요.\n")
                # driver.switch_to.frame(조회_프레임)
                # input()
                # manage.save(driver)
                # cid(driver, 기안)
            except:
                break
        # 기안 메뉴 loop end

        # 검색으로 돌아가기
        if first == True:
            continue

        # 기안 창으로 이동
        while True:
            try:
                driver.switch_to.window(driver.window_handles[1])
                break
            except:
                pass
        driver.switch_to.frame("message")

        # 테이블에서 기안 제목 및 금액 받아옴
        table = driver.find_element(by=By.ID, value="ctlTable")
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
        if re.match(".지출결의서.", title):
            기록물 = 용역
            if money >= 300000:
                결재 = 총결

        # 결재
        driver.switch_to.default_content()
        clickById(driver, 결재정보)
        driver.switch_to.frame(메인_프레임)
        clickById(driver, 즐겨찾기)
        clickById(driver, 결재)
        clickByXPath(driver, 적용)
        clickById(driver, 기록물철)
        clickById(driver, 기록물)
        clickByXPath(driver, 기안_확인)

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
    clickById(driver, 기안_파일버튼)
    time.sleep(0.5)
    path = 링크[3] + "기안 필요/"
    driver.switch_to.frame(메인_프레임)
    driver.switch_to.frame("dadiframe")
    for folder in os.listdir(path):
        searchKey = (
            "".join(folder.split("#")[:-1])
            .replace("$", "/")
            .replace("(", "\(")
            .replace(")", "\)")
            .strip()
        )
        if re.search(searchKey, title.strip()):
            draftFolder = path + folder + "/"

            # print(draftFolder)

            for file in os.listdir(draftFolder):
                abs_file_path = os.path.abspath(draftFolder + file)
                driver.find_element_by_xpath(기안_파일).send_keys(abs_file_path)

                # 로딩 안되고 올라가면 스킵되는 듯?
                time.sleep(1.5)
                print(file, "업로드 완료")
            if "완료" not in os.listdir(링크[3]):
                os.mkdir(링크[3] + "완료")
            os.replace(draftFolder, 링크[3] + "완료/" + folder)
            break
        else:
            print("기안 필요 폴더에 알맞은 폴더가 없습니다.")
            # 없을 시 완료 폴더에서 찾도록 변경
            uploaded = False
            path = 링크[3] + "완료/"
            for folder in os.listdir(path):
                searchKey = (
                    "".join(folder.split("#")[:-1])
                    .replace("$", "/")
                    .replace("(", "\(")
                    .replace(")", "\)")
                .strip())
                if re.search(searchKey, title.strip()):
                    draftFolder = path + folder + "/"

                    # print(draftFolder)

                    for file in os.listdir(draftFolder):
                        abs_file_path = os.path.abspath(draftFolder + file)
                        driver.find_element_by_xpath(기안_파일).send_keys(abs_file_path)

                        time.sleep(1.5)
                        print(file, "업로드 완료")
                        uploaded = True
                    break

                if not uploaded:
                    print("완료 필요 폴더에 알맞은 폴더가 없습니다\n파일 업로드 후 결재올림을 눌러주세요.")

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
    clickByXPath(driver, 닫기)
