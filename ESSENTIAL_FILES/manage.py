import datetime
import os
import re
import sys
import time

from datetime import *

from dateutil.relativedelta import *
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

from FUNC_LIBRARY.autoLogin import *
from HIDDEN_FILES.linkData import *
from FUNC_LIBRARY.alertController import *
from copy import deepcopy
from FUNC_LIBRARY import xlsxFileController, dateController, autoLogin, ignoreAutoLogout
import threading

sema = 0
d = ""
mod_month = "-1"


def refresh():
    clickByXPath(d, 조회)


def printProgress(i, max):
    c = int(i * max)
    sys.stdout.write(
        "\r[" + "#" * c + " " * (max - c - 1) + "]\t\t[" + str(int(i * 100)) + "%]"
    )


def monthly_textReplace(prev, month):
    r = re.compile("(\D*)([\d,]*\d+)(월)(\D*)")
    text_list = prev.split()
    result_string = ""

    for p in text_list:
        m = r.match(p)
        if m:
            result_string += re.sub(
                "(\D*)([\d,]*\d+)(월)(\D*)", "\g<1>" + month + "\g<3>\g<4> ", p
            )
        else:
            result_string += p + " "

    print(result_string)
    return result_string


def search(driver):
    global sema
    while True:
        print("회계 구분번호를 입력해주세요. ex) 1(등록금)/2(비등록금)/0(뒤로가기) ")
        print("검색이 필요 없으시면 엔터를 눌러주세요")
        acc = input().strip()
        if acc == "1" or acc == "2" or acc == "3":
            break
        elif acc == "":
            return
        print("잘못된 입력입니다.")
    if acc == "0":
        driver.switch_to.default_content()
        return

    while True:
        sema = 1
        print("결의서 구분번호를 입력해주세요. ex) 1(전체)/2(수입)/3(지출)/4(대체)")
        res = input().strip()
        if res == "1" or res == "2" or res == "3" or res == "4":
            break
        print("잘못된 입력입니다.")

    while True:
        print("원하시는 기간을 선택하세요. ex) 1/3/6/12/2022")
        month = input().strip()
        if len(month) == 1 or len(month) == 2 or len(month) == 4:
            break
        print("잘못된 입력입니다.")

    print("원하는 검색어를 입력해주세요. (없으면 공백)")
    srch = input().strip()

    if len(month) == 4:
        fillByName(driver, "txtSAcctYear", month)
    else:
        fillByName(driver, "txtSAcctYear", "2021")
    select = Select(driver.find_element_by_xpath(회계구분_조회))
    if acc == "1":
        select.select_by_index(0)
    elif acc == "2":
        select.select_by_index(1)

    select = Select(driver.find_element_by_xpath(결의서구분))
    if res == "1":
        select.select_by_index(0)
    elif res == "2":
        select.select_by_index(1)
    elif res == "3":
        select.select_by_index(2)
    elif res == "4":
        select.select_by_index(3)

    if month == "1":
        fillByName(driver, "DpFrDt", dateController.date1month())
    elif month == "3":
        fillByName(driver, "DpFrDt", dateController.date3month())
    elif month == "6":
        fillByName(driver, "DpFrDt", dateController.date6month())
    elif month == "12":
        fillByName(driver, "DpFrDt", dateController.date1year())
    elif len(month) == 4:
        # fname(driver, 'DpFrDt', month + '0301') 정책변경 -> 시작년도 2020년 고정
        fillByName(driver, "DpFrDt", "20200301")
        fillByName(driver, "DpToDt", str(int(month) + 1) + "0228")

    else:
        print("잘못된 입력입니다.")
    if len(month) != 4:
        fillByName(driver, "DpToDt", dateController.dateToday())
    fillByXPath(driver, 제목_검색, srch)
    clickByName(driver, "CSMenuButton1$List")


def lookup(driver):
    global sema
    global d
    d = driver
    ig = threading.Thread(target=ignoreAutoLogout.startTimer)
    ig.daemon = True
    ig.start()
    driver.switch_to.default_content()
    clickByXPath(driver, 결의서_조회)
    driver.switch_to.frame(조회_프레임)

    while True:
        while True:
            ignoreAutoLogout.timer = 0
            sema = 0
            search(driver)
            print("=====================================================")


def write(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(작성_프레임)

    print("\n=================================")
    while True:
        print("결의서를 작성하시겠습니까? 1(예)/2(아니오)")
        yes = input()
        if yes == "1":
            break

    file = xlsxFileController.load_xls(링크[2])
    input_data = xlsxFileController.all_data_fetch(file, "결의내역", "E15", "X15")
    w = 0
    prev = input_data[0][0]
    tax = 0

    target_data = input_data
    row = 15
    isMonthly = False
    title = ""

    # Main loop
    for i in range(len(target_data)):
        if target_data[i][0] != -1 or prev != -1:
            w = 1
            if prev != target_data[i][0]:
                try:
                    if tax == 1:
                        file = taxWrite(driver, prev, file, isMonthly, row)
                        tax = 0
                    row = 15 + i
                    isMonthly = False

                    save(driver)
                    if target_data[i][0] == -1:
                        prev = target_data[i][0]
                        continue

                    upload(driver, title)
                    clickByXPath(driver, 신규)
                    # time.sleep(0.5)

                    print("구분번호 :", target_data[i][0])
                    print("사업코드 입력 완료")
                except Exception as e:
                    print("예외가 발생했습니다:", str(e))
                    input("* 세금 계산 입력에 실패했습니다. 수동으로 입력 후 [Enter] 키를 입력해주세요")
                    sys.stdin.flush()

            print("-------- ", i + 15, "행 입력중입니다 --------", sep="")

            # 정기 체크
            if (
                target_data[i][1] is not None
                and target_data[i][1] != ""
                and target_data[i][1] != "_"
            ):
                isMonthly = True
                if target_data[i][2] != "" and target_data[i][2] != "_":
                    target_data[i][18] = str(target_data[i][18])
                    target_data[i][2] = str(target_data[i][2])
                    target_data[i][18] = monthly_textReplace(
                        target_data[i][18], target_data[i][2]
                    )

                    if (
                        target_data[i][3] is not None
                        and target_data[i][3] != ""
                        and target_data[i][3] != "_"
                    ):
                        target_data[i][3] = monthly_textReplace(
                            str(target_data[i][3]), target_data[i][2]
                        )

            time.sleep(0.5)
            if (
                target_data[i][4] is not None
                and target_data[i][4] != ""
                and target_data[i][4] != "_"
            ):
                target_data[i][4] = str(target_data[i][4])[:10]

            time.sleep(0.2)
            try:
                select = Select(driver.find_element_by_xpath(회계구분_작성))
                if (
                    target_data[i][5] is not None
                    and target_data[i][5] != ""
                    and target_data[i][5] != "_"
                ):
                    if target_data[i][5] == "등록금":
                        select.select_by_index(0)
                    elif target_data[i][5] == "비등록금" or target_data[i][5] == "(서울)기숙사":
                        select.select_by_index(1)
                    time.sleep(0.2)
                print("회계 구분 입력 완료")
            except Exception as e:
                print("예외가 발생했습니다:", str(e))
                input("* 회계 구분 입력에 실패했습니다. 수동으로 입력 후 [Enter] 키를 입력해주세요")
                sys.stdin.flush()

            try:
                if (
                    target_data[i][4] is not None
                    and target_data[i][4] != ""
                    and target_data[i][4] != "_"
                ):
                    fillByXPath(driver, 결의일자_번호, target_data[i][4])
                select = Select(driver.find_element_by_id("ddlResolutionDiv"))
                print("결의일자 번호 입력 완료")
            except Exception as e:
                print("예외가 발생했습니다:", str(e))
                input("* 결의일자 번호 입력에 실패했습니다. 수동으로 입력 후 [Enter] 키를 입력해주세요")
                sys.stdin.flush()

            try:
                if (
                    target_data[i][6] is not None
                    and target_data[i][6] != ""
                    and target_data[i][6] != "_"
                ):
                    test3 = {"수입": 0, "지출": 1, "대체": 2}
                    select.select_by_index(test3[target_data[i][6]])

                    fillByXPath(driver, 사업코드, target_data[i][5])
                    enterByXPath(driver, 사업코드)
                    driver.switch_to.frame("frmPopup")
                    enterByXPath(driver, 사업팝업)
                    driver.switch_to.default_content()
                    driver.switch_to.frame("ifr_d4_AHG020P")
                print("사업코드 입력 완료")
            except:
                input("* 사업코드 입력에 실패했습니다. 수동으로 입력 후 [Enter] 키를 입력해주세요")
                sys.stdin.flush()

            try:
                if (
                    target_data[i][3] is not None
                    and target_data[i][3] != ""
                    and target_data[i][3] != "_"
                ):
                    fillByXPath(driver, 결의서_제목, target_data[i][3])
                    title = target_data[i][3]
                fillByXPath(driver, 계정과목, target_data[i][8])
                enterByXPath(driver, 계정과목)
                print("계정과목 입력 완료")
            except Exception as e:
                print("예외가 발생했습니다:", str(e))
                input("* 계정과목 입력에 실패했습니다. 수동으로 입력 후 [Enter] 키를 입력해주세요")
                sys.stdin.flush()

            try:
                if (
                    target_data[i][9] is not None
                    and target_data[i][9] != ""
                    and target_data[i][9] != "_"
                ):
                    fillByXPath(driver, 관리코드, target_data[i][9])
                    enterByXPath(driver, 관리코드)
                    time.sleep(0.2)
                    try:
                        driver.switch_to.alert.accept() # 관리코드 입력이 필요없는 경우
                        print("관리코드가 필요없는 자료")
                    except:
                        driver.switch_to.frame("frmPopup")
                        enterByXPath(driver, 관리팝업)  # 입력이 바로 될 경우
                        time.sleep(1)
                        driver.switch_to.default_content()
                        driver.switch_to.frame("ifr_d4_AHG020P")
                        관리코드값 = driver.find_element(By.NAME, "txtDetailMngrCode").get_attribute("value")
                        if not 관리코드값:
                            raise ValueError("관리코드가 비어있음")

                    if not driver.find_element(By.NAME, "txtDetailMngrName").get_attribute("value"):
                        raise ValueError("관리코드 텍스트이 비어있음")
                    print("관리코드 입력 완료")
                else:
                    raise ValueError("엑셀: [%d 행]의 관리코드가 비어있음" % (i + 15))
            except Exception as e:
                print("예외가 발생했습니다:", str(e))
                input("* 관리코드 입력에 실패했습니다. 수동으로 입력 후 [Enter] 키를 입력해주세요")
                sys.stdin.flush()

            try:
                if target_data[i][11] is not None and target_data[i][11] != "" and target_data[i][11] != "_":
                    # 귀속부서가 기숙사일 경우 2개의 결과가 있어 직접 코드를 입력해야 한다
                    if target_data[i][11] == "기숙사":
                        fillByXPath(driver, 귀속부서, "")
                        enterByXPath(driver, 귀속부서)
                        try:
                            driver.switch_to.alert.accept()
                        except:
                            driver.switch_to.frame("frmPopup")
                            enterByXPath(driver, 귀속부서팝업)
                            fillByXPath(driver, 소속코드, "A33100")
                            enterByXPath(driver, 소속코드)
                            time.sleep(0.3)
                            actions = ActionChains(driver)
                            doubleClick = driver.find_element_by_xpath(소속테이블)
                            actions.move_to_element(doubleClick)
                            actions.double_click(doubleClick)
                            actions.perform()

                    else:
                        fillByXPath(driver, 귀속부서, target_data[i][11])
                        enterByXPath(driver, 귀속부서)

                    driver.switch_to.default_content()
                    driver.switch_to.frame("ifr_d4_AHG020P")

                time.sleep(0.3)
                귀속부서값 = driver.find_element(By.NAME, "txtDetailSosogCd").get_attribute("value")
                if not 귀속부서값:
                    raise ValueError("귀속부서가 비어있음")

                print("귀속부서 입력 완료")
            except Exception as e:
                print("예외가 발생했습니다:", str(e))
                input("* 귀속부서 입력에 실패했습니다. 수동으로 입력 후 [Enter] 키를 입력해주세요")
                sys.stdin.flush()

            try:
                select = Select(driver.find_element_by_id("ddlDetailEvidenceGb"))
                test2 = {"없음": 0, "세금": 1, "기타": 2, "현금": 3}
                select.select_by_index(test2[target_data[i][13]])

                지출차변금액 = target_data[i][16]
                수입대변금액 = target_data[i][17]
                적요사항 = target_data[i][18]
                integer_value = None
                if 지출차변금액 is not None and 지출차변금액 != "" and 지출차변금액 != "_":
                    if isinstance(지출차변금액, int):
                        integer_value = 지출차변금액
                    elif isinstance(지출차변금액, float):
                        rounded_value = round(지출차변금액)
                        integer_value = int(rounded_value)
                    fillByXPath(driver, 지출, integer_value)
                if 수입대변금액 is not None and 수입대변금액 != "" and 수입대변금액 != "_":
                    integer_value = None
                    if isinstance(수입대변금액, int):
                        integer_value = 수입대변금액
                    elif isinstance(수입대변금액, float):
                        rounded_value = round(수입대변금액)
                        integer_value = int(rounded_value)
                    fillByXPath(driver, 수입, str(integer_value))
                if 적요사항 is not None and 적요사항 != "" and 적요사항 != "_":
                    fillByXPath(driver, 적요, 적요사항)
                print("금액 입력 완료")
            except Exception as e:
                print("예외가 발생했습니다:", str(e))
                input("* 금액(적요) 입력에 실패했습니다. 수동으로 입력 후 [Enter] 키를 입력해주세요")
                sys.stdin.flush()

            # time.sleep(0.2)
            clickByXPath(driver, 결의내역_제출)
            time.sleep(0.3)

            if target_data[i][13] == "세금":
                tax = 1
                dismissAlert(driver)

        prev = target_data[i][0]

        if i == len(target_data) - 1 and w == 1:
            if tax == 1:
                file = taxWrite(driver, prev, file, isMonthly, row)
                tax = 0

            save(driver)
            upload(driver, title)

            print("입력이 완료되었습니다.")
            print("구분번호 미변경시 중복 입력될 수 있으니 확인 부탁드립니다.")


def taxWrite(driver, num, file, isMonthly, row):
    try:
        time.sleep(0.3)
        clickByXPath(driver, 세금계산_탭)
        tax_data = xlsxFileController.all_data_fetch(
            file, "결의내역", "AB" + str(row), "AJ" + str(row)
        )
        for j in range(len(tax_data)):
            if tax_data[j][0] == num:
                test = {
                    "매입세금-불": 1,
                    "매입세금": 2,
                    "매입계산": 3,
                    "매출세금": 4,
                    "매출계산": 5,
                    "매출세금-불": 6,
                    "수입세금": 7,
                    "수입계산": 8,
                    "매입세금-간": 9,
                }
                select = Select(driver.find_element_by_xpath(과세구분))
                select.select_by_index(test[tax_data[j][1]])
                fillByXPath(driver, 발행일자, tax_data[j][2].strftime("%Y%m%d"))
                enterByXPath(driver, 발행일자)
                fillByXPath(driver, 거래처, "")
                enterByXPath(driver, 거래처)
                time.sleep(0.5)  # 없어도 돌아가긴 함
                driver.switch_to.frame("frmPopup")
                if 48 <= ord(str(tax_data[j][3])[0]) <= 57:
                    fillByXPath(driver, 사업자번호, tax_data[j][3])
                    enterByXPath(driver, 사업자번호)
                else:
                    fillByXPath(driver, 거래처명, tax_data[j][3])
                    enterByXPath(driver, 거래처명)
                driver.switch_to.default_content()
                driver.switch_to.frame("ifr_d4_AHG020P")
                if (
                    tax_data[j][4] is not None
                    and tax_data[j][4] != ""
                    and tax_data[j][4] != "_"
                ):
                    fillByXPath(driver, 공급가액, tax_data[j][4])
                    fillByXPath(driver, 세액, tax_data[j][5])

                select = Select(driver.find_element_by_id("ddlBillDiv"))
                test1 = {"일반": 1, "전자": 2, "현금": 3}
                select.select_by_index(test1[tax_data[j][6]])
                clickByXPath(driver, 세금계산_제출)
                time.sleep(0.5)
        # for p in range(len(tax_data)):
        #     if tax_data[p][0] == num:
        #         if isMonthly:
        #             xlsxFileController.put_cell_data(file, '결의내역', 'AB' + str(p+row), -1)
        #         else:
        #             xlsxFileController.put_cell_data(file, '세금계산', 'E' + str(p+20), -1)
        clickByXPath(driver, 결의내역_탭)
        print("세금처리가 완료되었습니다.")
    except:
        print("오류")
        return
    return file


def upload(driver, title):
    path = ""
    for inFolder in os.listdir(링크[3] + "결의서 작성 필요/"):
        checkFolder = "".join(inFolder.split("#")[:-1])
        if checkFolder.replace("$", "/").strip() == title.strip():
            path = 링크[3] + "결의서 작성 필요/" + inFolder + "/"
            dpath = 링크[3] + "기안 필요/" + inFolder + "/"
            break

    if path:
        clickByXPath(driver, 첨부파일)
        driver.switch_to.window(driver.window_handles[1])
        for f in os.listdir(path):
            abs_file_path = os.path.abspath(path + f)
            time.sleep(1)
            driver.find_element_by_xpath(파일선택).send_keys(abs_file_path)
            time.sleep(0.5)
            clickByXPath(driver, 파일업로드)
            print(f, "파일 업로드 완료")

        os.replace(path, dpath)
        print("첨부된 파일이 ( 기안 필요 ) 폴더로 이동되었습니다.")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(0.1)
        driver.switch_to.frame(작성_프레임)
        save(driver)


def save(driver):
    while True:
        # print("저장하시겠습니까? 1(예)/ 2(아니오)")
        # sv = input()
        sv = "1"
        if sv == "1":
            break
        else:
            time.sleep(3)
    clickByXPath(driver, 저장)
    time.sleep(0.3)
    acceptAlert(driver)


def delete(file):
    print("입력된 데이터를 전부 삭제하겠습니까? 1(예)/2(아니오)")
    d = input().strip()
    if d == "1":
        xlsxFileController.delete_completed_row(file, "결의내역", "E", "Y", 15)
        xlsxFileController.delete_completed_row(file, "세금계산", "E", "L", 20)
        # xlsxFileController.save_xls(file)
        print("삭제가 완료되었습니다.")

# 다음달로 복사 후 기안
def modify(driver, isDraft: bool):
    global sema
    global d

    if not isDraft:
        d = driver
        ig = threading.Thread(target=ignoreAutoLogout.startTimer)
        ig.daemon = True
        ig.start()
        clickByXPath(driver, 결의서_조회)

    while True:
        if not isDraft:
            modify_input()

        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)
        driver.switch_to.frame("frmPopup")

        # 결의서 제목 및 날짜 저장
        title = []
        res_summary = []
        tax_date = []

        # title[0] 나중에 변경 해야함
        title.append("temp")
        # res_date = driver.find_element_by_xpath(결의일자_번호)
        # title.append(res_date.get_attribute("value"))
        res_title = driver.find_element_by_xpath(결의서_제목)
        title.append(res_title.get_attribute("value"))

        # 필요 없어짐
        # # 결의서 날짜 변경
        # change = str(int(title[0][5:7])%12 + 1)
        # if int(change) < 10:
        #     change = "0" + change
        # title[0] = title[0][:5] + change + title[0][7:]
        #
        # # 달마다 없는 날짜 처리
        # if int(change) == 1:
        #     if int(title[0][8:]) > 28:
        #         title[0] = title[0][:8] + str(28)
        # if int(title[0][8:]) == 31:
        #     if int(change) != 7:
        #         title[0] = title[0][:8] + str(30)

        # 복사 창 이동
        clickByXPath(driver, 복사)
        # alert = driver.switch_to.alert
        # alert.send_keys(title[0])

        while True:
            try:
                alert = driver.switch_to.alert
                time.sleep(0.5)
            except:
                break

        # for _ in range(3):
        #     acceptAlert(driver)

        res_date = driver.find_element_by_xpath(결의일자_번호)
        title[0] = res_date.get_attribute("value")

        # 내부 데이터 수집 (결의항목)
        table = driver.find_element_by_xpath(결의서_테이블)
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        for tr in tbody.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            i = 0
            for td in tr.find_elements(by=By.TAG_NAME, value="td"):
                i += 1
                if i == 10:
                    res_summary.append(td.get_attribute("innerText"))

        # 내부 데이터 수집 (세금)
        table = driver.find_element_by_xpath(세금계산_테이블)
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        for tr in tbody.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            i = 0
            for td in tr.find_elements(by=By.TAG_NAME, value="td"):
                i += 1
                if i == 4:
                    tax_date.append(td.get_attribute("innerText"))

        ##
        ## 연도 제거
        ##
        title[1] = delete_year_str(title[1])
        title[1] = monthly_check(title[1]).strip()
        for i in range(len(res_summary)):
            res_summary[i] = monthly_check_for_summary(res_summary[i], title[1])
        print("결의서 날짜 + 제목", title, "", "적요", *res_summary, "", sep="\n")
        # 날짜 및 제목 입력
        # time.sleep(0.5)
        fillByXPath(driver, 집행요청일, title[0])
        enterByXPath(driver, 집행요청일)
        time.sleep(0.3)
        # fpath(driver, 지급예정일, title[0])
        # epath(driver, 지급예정일)
        # acceptAlert(driver)
        fillByXPath(driver, 결의서_제목, title[1])
        driver.find_element_by_xpath(세부사항).clear()

        # 결의서 작성
        for i in range(len(res_summary)):
            clickByXPath(driver, 결의서_링크 + "[" + str(i + 2) + "]")
            fillByXPath(driver, 적요, res_summary[i])
            clickByXPath(driver, 결의내역_제출)
            time.sleep(0.1)

        # 세금 작성
        if tax_date and tax_date[0] != "":
            clickByXPath(driver, 세금계산_탭)

            try:
                # dateutil 로 대체
                for i in range(len(tax_date)):
                    tax_date[i] = datetime.strptime(
                        tax_date[i], "%Y-%m-%d"
                    ) + relativedelta(months=1)
                    tax_date[i] = datetime.strftime(tax_date[i], "%Y-%m-%d")

                print("세금 날짜", *tax_date, "", sep="\n")

                # 세금 작성
                for i in range(len(tax_date)):
                    clickByXPath(driver, 세금계산_링크 + "[" + str(i + 2) + "]")
                    fillByXPath(driver, 발행일자, tax_date[i])
                    clickByXPath(driver, 세금계산_제출)
                    time.sleep(0.1)
            except:
                print("세금 날짜 작성에 실패하였습니다")
            clickByXPath(driver, 결의내역_탭)

        save(driver)
        print("저장이 완료되었습니다.")

        mkdir_if_not_exist()

        modify_draft(title[1])
        path = ""
        dpath = ""
        try:
            for inFolder in os.listdir(링크[3] + "결의서 작성 필요/"):
                checkFolder = "".join(inFolder.split("#")[:-1])
                if checkFolder.replace("$", "/").strip() == title[1].strip():
                    path = 링크[3] + "결의서 작성 필요/" + inFolder + "/"
                    dpath = 링크[3] + "기안 필요/" + inFolder + "/"
                    break
        except:
            print("경로 설정 오류 - 파일 저장에 실패했습니다")
            pass

        print("path:", path)

        if path:
            clickByXPath(driver, 첨부파일)
            driver.switch_to.window(driver.window_handles[1])
            for f in os.listdir(path):
                abs_file_path = os.path.abspath(path + f)
                time.sleep(1)
                driver.find_element_by_xpath(파일선택).send_keys(abs_file_path)
                time.sleep(0.5)
                clickByXPath(driver, 파일업로드)
                print(f, "파일 업로드 완료")

            try:
                os.replace(path, dpath)
                print("첨부된 파일이 ( 기안 필요 ) 폴더로 이동되었습니다.")
            except:
                print("경로 설정 오류 - 기안 필요 파일 이동에 실패했습니다")
                pass

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.1)
            driver.switch_to.frame(조회_프레임)

            # 해야함
            driver.switch_to.frame("frmPopup")
            save(driver)
        else:
            print("파일을 찾을 수 없습니다")
            print("파일을 올리고 저장 후 엔터를 눌러주세요.")
            input()
        # print("작성되었습니다.\n저장하시겠습니까? 1(예)/2(아니오)")
        # s = input()
        # if s == '1':
        #     save(driver)
        #     print("저장이 완료되었습니다.")
        #
        # else:
        #     print("원하시는 버튼을 입력해주세요. 1(저장) 2(창 닫고 재시작)")
        #     put = input()
        #     while put != '1' and put != '2':
        #         print("잘못된 입력입니다.")
        #         put = input()
        #     if put == '1':
        #         save(driver)
        #         print("저장이 완료되었습니다.")
        #     if put == '2':
        #         break

        # Draft에서 실행된 경우
        if isDraft:
            return
        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)
        clickByXPath(driver, 닫기)
        time.sleep(1)

        print("\n=====================================================")

def modify_month(driver, month: int): # 특정 월로 복사 후 기안
    global sema
    global d

    while True:
        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)
        driver.switch_to.frame("frmPopup")

        # 결의서 제목 및 날짜 저장
        title = []
        res = []
        tax_date = []

        title.append("temp")
        res_title = driver.find_element_by_xpath(결의서_제목)
        title.append(res_title.get_attribute("value"))

        clickByXPath(driver, 복사)

        while True:
            try:
                alert = driver.switch_to.alert
                time.sleep(0.5)
            except:
                break

        res_date = driver.find_element_by_xpath(결의일자_번호)
        title[0] = res_date.get_attribute("value")

        # 내부 데이터 수집 (결의항목)
        table = driver.find_element_by_xpath(결의서_테이블)
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        for tr in tbody.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            i = 0
            for td in tr.find_elements(by=By.TAG_NAME, value="td"):
                i += 1
                if i == 10:
                    res.append(td.get_attribute("innerText"))

        # 내부 데이터 수집 (세금)
        table = driver.find_element_by_xpath(세금계산_테이블)
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        for tr in tbody.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            i = 0
            for td in tr.find_elements(by=By.TAG_NAME, value="td"):
                i += 1
                if i == 4:
                    tax_date.append(td.get_attribute("innerText"))

        # 연도 제거
        title[1] = delete_year_str(title[1])
        title[1] = change_month(title[1], month).strip()
        for i in range(len(res)):
            res[i] = change_month(res[i], month) # 월 변경
        print("결의서 날짜 + 제목", title, "", "적요", *res, "", sep="\n")

        # 날짜 및 제목 입력
        fillByXPath(driver, 집행요청일, title[0])
        enterByXPath(driver, 집행요청일)
        time.sleep(0.3)
        fillByXPath(driver, 결의서_제목, title[1])
        driver.find_element_by_xpath(세부사항).clear()

        # 결의서 작성
        for i in range(len(res)):
            clickByXPath(driver, 결의서_링크 + "[" + str(i + 2) + "]")
            fillByXPath(driver, 적요, res[i])
            clickByXPath(driver, 결의내역_제출)
            time.sleep(0.1)

        # 세금 작성
        if tax_date and tax_date[0] != "":
            clickByXPath(driver, 세금계산_탭)

            try:
                # dateutil 로 대체
                for i in range(len(tax_date)):
                    tax_date[i] = datetime.strptime(
                        tax_date[i], "%Y-%m-%d"
                    ) + relativedelta(months=1)
                    tax_date[i] = datetime.strftime(tax_date[i], "%Y-%m-%d")

                print("세금 날짜", *tax_date, "", sep="\n")

                # 세금 작성
                for i in range(len(tax_date)):
                    clickByXPath(driver, 세금계산_링크 + "[" + str(i + 2) + "]")
                    fillByXPath(driver, 발행일자, tax_date[i])
                    clickByXPath(driver, 세금계산_제출)
                    time.sleep(0.1)
            except:
                print("세금 날짜 작성에 실패하였습니다")
            clickByXPath(driver, 결의내역_탭)

        save(driver)
        print("저장이 완료되었습니다.")

        mkdir_if_not_exist()

        modify_draft(title[1])
        path = ""
        depth = ""
        try:
            for inFolder in os.listdir(링크[3] + "결의서 작성 필요/"):
                checkFolder = "".join(inFolder.split("#")[:-1])
                if checkFolder.replace("$", "/").strip() == title[1].strip():
                    path = 링크[3] + "결의서 작성 필요/" + inFolder + "/"
                    dpath = 링크[3] + "기안 필요/" + inFolder + "/"
                    break
        except:
            print("경로 설정 오류 - 파일 저장에 실패했습니다")
            pass

        print("path:", path)

        if path:
            clickByXPath(driver, 첨부파일)
            driver.switch_to.window(driver.window_handles[1])
            for f in os.listdir(path):
                abs_file_path = os.path.abspath(path + f)
                driver.find_element_by_xpath(파일선택).send_keys(abs_file_path)
                time.sleep(0.3)
                clickByXPath(driver, 파일업로드)
                print(f, "파일 업로드 완료")

            try:
                os.replace(path, dpath)
                print("첨부된 파일이 ( 기안 필요 ) 폴더로 이동되었습니다.")
            except:
                print("경로 설정 오류 - 기안 필요 파일 이동에 실패했습니다")
                pass

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.1)
            driver.switch_to.frame(조회_프레임)

            # 해야함
            driver.switch_to.frame("frmPopup")
            save(driver)
        else:
            print("파일을 찾을 수 없습니다")
            print("파일을 올리고 저장 후 엔터를 눌러주세요.")
            input()

        driver.switch_to.default_content()
        # driver.switch_to.frame(조회_프레임)
        # clickByXPath(driver, 닫기)
        time.sleep(1)

        print("\n=====================================================")
        break

# 다음달로 복사 후 미지급금 기안
def modify_non_paid(driver, isDraft: bool):
    global sema
    global d

    if not isDraft:
        d = driver
        ig = threading.Thread(target=ignoreAutoLogout.startTimer)
        ig.daemon = True
        ig.start()
        clickByXPath(driver, 결의서_조회)

    while True:
        if not isDraft:
            modify_input()

        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)
        driver.switch_to.frame("frmPopup")

        # 결의서 제목 및 날짜 저장
        title = []
        res = []
        tax_date = []

        # title[0] 나중에 변경 해야함
        title.append("temp")
        res_title = driver.find_element_by_xpath(결의서_제목)
        title.append(res_title.get_attribute("value"))

        # 복사 창 이동
        clickByXPath(driver, 복사)

        while True:
            try:
                alert = driver.switch_to.alert
                time.sleep(0.5)
            except:
                break

        res_date = driver.find_element_by_xpath(결의일자_번호)
        title[0] = res_date.get_attribute("value")

        # 내부 데이터 수집 (결의항목)
        table = driver.find_element_by_xpath(결의서_테이블)
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        for tr in tbody.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            i = 0
            for td in tr.find_elements(by=By.TAG_NAME, value="td"):
                i += 1
                if i == 10:
                    res.append(td.get_attribute("innerText"))

        # 내부 데이터 수집 (세금)
        table = driver.find_element_by_xpath(세금계산_테이블)
        tbody = table.find_element(by=By.TAG_NAME, value="tbody")
        for tr in tbody.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            i = 0
            for td in tr.find_elements(by=By.TAG_NAME, value="td"):
                i += 1
                if i == 4:
                    tax_date.append(td.get_attribute("innerText"))

        ##
        ## 연도 제거
        ##
        title[1] = delete_year_str(title[1])

        title[1] = monthly_check(title[1]).strip()

        for i in range(len(res)):
            res[i] = monthly_check_item(res[i], title[1])
        print("결의서 날짜 + 제목", title, "", "적요", *res, "", sep="\n")
        # 날짜 및 제목 입력
        # time.sleep(0.5)
        fillByXPath(driver, 집행요청일, title[0])
        enterByXPath(driver, 집행요청일)
        time.sleep(0.3)
        # fpath(driver, 지급예정일, title[0])
        # epath(driver, 지급예정일)
        # acceptAlert(driver)
        fillByXPath(driver, 결의서_제목, title[1])
        driver.find_element_by_xpath(세부사항).clear()

        # 결의서 작성
        for i in range(len(res)):
            clickByXPath(driver, 결의서_링크 + "[" + str(i + 2) + "]")
            fillByXPath(driver, 적요, res[i])
            clickByXPath(driver, 결의내역_제출)
            time.sleep(0.1)

        # 세금 작성
        if tax_date and tax_date[0] != "":
            clickByXPath(driver, 세금계산_탭)

            try:
                # dateutil 로 대체
                for i in range(len(tax_date)):
                    tax_date[i] = datetime.strptime(
                        tax_date[i], "%Y-%m-%d"
                    ) + relativedelta(months=1)
                    tax_date[i] = datetime.strftime(tax_date[i], "%Y-%m-%d")

                print("세금 날짜", *tax_date, "", sep="\n")

                # 세금 작성
                for i in range(len(tax_date)):
                    clickByXPath(driver, 세금계산_링크 + "[" + str(i + 2) + "]")
                    fillByXPath(driver, 발행일자, tax_date[i])
                    clickByXPath(driver, 세금계산_제출)
                    time.sleep(0.1)
            except:
                print("세금 날짜 작성에 실패하였습니다")
            clickByXPath(driver, 결의내역_탭)

        save(driver)
        print("저장이 완료되었습니다.")

        mkdir_if_not_exist()

        modify_draft(title[1])
        path = ""
        depth = ""
        try:
            for inFolder in os.listdir(링크[3] + "결의서 작성 필요/"):
                checkFolder = "".join(inFolder.split("#")[:-1])
                if checkFolder.replace("$", "/").strip() == title[1].strip():
                    path = 링크[3] + "결의서 작성 필요/" + inFolder + "/"
                    dpath = 링크[3] + "기안 필요/" + inFolder + "/"
                    break
        except:
            print("경로 설정 오류 - 파일 저장에 실패했습니다")
            pass

        print("path:", path)

        if path:
            clickByXPath(driver, 첨부파일)
            driver.switch_to.window(driver.window_handles[1])
            for f in os.listdir(path):
                abs_file_path = os.path.abspath(path + f)
                driver.find_element_by_xpath(파일선택).send_keys(abs_file_path)
                time.sleep(0.3)
                clickByXPath(driver, 파일업로드)
                print(f, "파일 업로드 완료")

            try:
                os.replace(path, dpath)
                print("첨부된 파일이 ( 기안 필요 ) 폴더로 이동되었습니다.")
            except:
                print("경로 설정 오류 - 기안 필요 파일 이동에 실패했습니다")
                pass

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.1)
            driver.switch_to.frame(조회_프레임)

            # 해야함
            driver.switch_to.frame("frmPopup")
            save(driver)
        else:
            print("파일을 찾을 수 없습니다")
            print("파일을 올리고 저장 후 엔터를 눌러주세요.")
            input()
        # print("작성되었습니다.\n저장하시겠습니까? 1(예)/2(아니오)")
        # s = input()
        # if s == '1':
        #     save(driver)
        #     print("저장이 완료되었습니다.")
        #
        # else:
        #     print("원하시는 버튼을 입력해주세요. 1(저장) 2(창 닫고 재시작)")
        #     put = input()
        #     while put != '1' and put != '2':
        #         print("잘못된 입력입니다.")
        #         put = input()
        #     if put == '1':
        #         save(driver)
        #         print("저장이 완료되었습니다.")
        #     if put == '2':
        #         break

        # Draft에서 실행된 경우
        if isDraft:
            return
        driver.switch_to.default_content()
        driver.switch_to.frame(조회_프레임)
        clickByXPath(driver, 닫기)
        time.sleep(1)

        print("\n=====================================================")


def mkdir_if_not_exist():
    target_dir = "./완료"
    standard_dir = "./기준"
    need_dir = "./결의서 작성 필요"
    draft_dir = "./기안 필요"
    input_dir = "./in"

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    if not os.path.exists(standard_dir):
        os.mkdir(standard_dir)
    if not os.path.exists(need_dir):
        os.mkdir(need_dir)
    if not os.path.exists(draft_dir):
        os.mkdir(draft_dir)
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)


# in에 있는거를 결의서 작성필요로
def modify_draft(title):
    target_dir = "./기준"
    need_dir = "./결의서 작성 필요"
    draft_dir = "./기안 필요"
    input_dir = "./in"

    find_modify_list = []
    find_draft_list = []

    # 기준에서 폴더찾고 안에서 파일이름 가져오기
    for modify_folder in os.listdir(target_dir):
        modify_title = "".join(modify_folder.split("#")[:-1])
        # 폴더 제목에서 %d월 형식의 숫자 제외하기 (결의서 제목으로 기준에서 찾아)

        if delete_month(modify_title) == delete_month(title.replace("/", "$")):
            # %d월 형식 제외한 title과 비교하여 일치하면 폴더 진입
            for pdf in os.listdir(target_dir + "/" + modify_folder):
                # 폴더 내 pdf 파일의 %d월 형식 제외
                print("기준 파일 match : [", delete_month(pdf), "]")
                find_modify_list.append(delete_month(pdf))
            break

    # 기준에서 찾은 파일이름과 똑같은 이름인거 in에서 가져오기
    for pdf in os.listdir(input_dir):
        # print("findmodifylist, pdf : ", find_modify_list, pdf, delete_month(pdf))
        if delete_month(pdf) in find_modify_list:
            find_draft_list.append(pdf)
    draft_folder = need_dir + "/" + title.replace("/", "$") + "#_/"

    if title.replace("/", "$") + "#_" not in os.listdir(need_dir):
        os.mkdir(draft_folder)
    for draft_file in find_draft_list:
        os.replace(input_dir + "/" + draft_file, draft_folder + draft_file)

    # 일치하는 pdf 파일을 modify 할 때 업로드 후 기안 필요 폴더에 넣기


def delete_month(name):
    flag = re.compile("(\d)+월")
    name = re.sub(flag, "월", name)
    return name


# TODO
#   /d/d? 꼴로 바꾸기
def monthly_textReplace(prev, month):
    r = re.compile("(\D*)([\d,]*\d+)(월)(\D*)")
    text_list = prev.split()
    result_string = ""

    for p in text_list:
        m = r.match(p)
        if m:
            result_string += re.sub(
                "(\D*)([\d,]*\d+)(월)(\D*)", "\g<1>" + month + "\g<3>\g<4> ", p
            )
        else:
            result_string += p + " "

    return result_string


def modify_input():
    print("변경하실 페이지를 띄우신 후 엔터를 눌러주세요")
    input()

    # global mod_month
    # while True:
    # print("변경하실 페이지를 띄우신 후 변경하실 월을 입력해주세요")
    # print("변경하실 월을 입력해주세요")
    # month = input()
    # if re.fullmatch(r'(\D*)([\d,]*\d+)', month):
    #     break
    # print("잘못된 입력입니다.")
    # mod_month = month
    # return month


def month_inc(month, val):
    ret = []
    for m in month:
        new_month = int(m) + val
        if new_month > 12:
            new_month %= 12
        ret.append(str(new_month))

    return ret


def ymonth_inc(ymonth, val):
    ret = []
    print(" : ", ymonth)
    t = ymonth[0]
    for m in ymonth[0][1]:
        nm = m + val
        if nm > 12:
            nm %= 12
            t = ymonth[0][0] + 1
        ret.append(nm)
    r = [t]
    r.append(ret)
    return r


def delete_year_str(string):
    y_space = re.compile("(\d*)( 년)")
    ydo_back = re.compile("(\d*)(년도 )")
    ydo_space = re.compile("(\d*)( 년도)")
    ydo = re.compile("(\d*)(년도)")
    y_back = re.compile("(\d*)(년 )")
    y = re.compile("(\d*)(년)")
    y_ = re.compile("(\d+)(년)(분*)")

    ret = string
    ret = re.sub(ydo_back, "", ret)
    ret = re.sub(ydo_space, "", ret)
    ret = re.sub(ydo, "", ret)
    ret = re.sub(y_space, "", ret)
    ret = re.sub(y_back, "", ret)
    ret = re.sub(y, "", ret)
    ret = re.sub(y_, "", ret)

    return ret


def monthly_check(prev):
    r = re.compile("(\D*)([\d,]*\d+)(월)(\D*)")
    q2 = re.compile("(\D*)([\d~]*\d+)(월)(\D*)")
    n = re.compile(("\d[ , ]+\d"))
    q = re.compile(("(\d*)~(\d*)"))
    y = re.compile("(\d*)(년)")
    # yy = re.compile('(\d*)( 년)')
    # yyy = re.compile('(\d*)(년 )')
    # only_y = re.compile('(\d+)(년)(분*)')
    c = re.compile("[']*(\d*)\.(\d*)\.(\d*)(\.)*")

    prev = delete_year_str(prev)

    # Key : 0 == 일반적인 케이스 / 1 == 연속된 달 / 2 == 분기
    l, key = 0, 0
    ret = []
    ret_y = []

    text_list = prev.split()
    pprev = ""

    result = ""

    for p in text_list:
        if c.search(p):
            f = c.findall(p)
            if len(f) == 2:
                date1 = datetime.datetime(int(f[0][0]), int(f[0][1]), int(f[0][2]))
                date2 = datetime.datetime(int(f[1][0]), int(f[1][1]), int(f[1][2]))
                if dateController.date2dateByDays(date1, date2) > 300:
                    # 1년 단위 차이라고 가정
                    # year_gap = dateController.date2dateByYears(date1,date2)
                    year_gap = round(dateController.date2dateByDays(date1, date2) / 365)
                    t = re.sub(
                        "[']*(\d*)\.(\d*)\.(\d*)(\.)*[~\-][']*(\d*)\.(\d*)\.(\d*)(\.)*",
                        dateController.jumpDateByYear(date1, year_gap)
                        + "~"
                        + dateController.jumpDateByYear(date2, year_gap),
                        p,
                    )
                    result += t + " "
                    # result += dateController.jumpDateByYear(date1,year_gap)+"~"+dateController.jumpDateByYear(date2,year_gap)
                elif dateController.date2dateByDays(date1, date2) > 31:
                    month_gap = round(dateController.date2dateByDays(date1, date2) / 31)
                    t = re.sub(
                        "[']*(\d*)\.(\d*)\.(\d*)(\.)*[~\-][']*(\d*)\.(\d*)\.(\d*)(\.)*",
                        dateController.jumpDateByMonth(date1, month_gap)
                        + "~"
                        + dateController.jumpDateByMonth(date2, month_gap),
                        p,
                    )
                    result += t + " "
            elif len(f) == 1:
                result += p + " "
        else:
            check = False
            # 년도가 등장하는 부분 시작
            if (y.match(pprev) and r.match(p)) or (y.match(pprev) and q2.match(p)):
                # print(pprev)
                temp = []
                m = l
                x = []
                while m < l + len(p):
                    if "0" <= prev[m] <= "9":
                        s = prev[m]
                        if "0" <= prev[m + 1] <= "9":
                            s += prev[m + 1]
                            m += 1
                        x.append(int(s))
                    m += 1
                for tmp in temp:
                    x.append(int(s))
                ret_y.append([int(pprev[:-1]), x])
                # year_part = pprev
                # 연도 붙이기
                # print("ret_y = " + str(ret_y))
            # 년도가 등장하는 부분 종료
            elif r.match(p) or q2.match(p) or q.match(p):
                temp = []
                m = l
                while m < l + len(p):
                    if "0" <= prev[m] <= "9":
                        s = prev[m]
                        if "0" <= prev[m + 1] <= "9":
                            s += prev[m + 1]
                            m += 1
                        temp.append(s)
                    m += 1
                ret.append(temp)

            l += len(p) + 1
            pprev = p
            # print(pprev)

        if not check:
            # print(p, ret_y)
            # print(p, ret)

            if q.search(p):
                key = 2
            if(key == 2):
                first_month = int(ret[0][0])
                second_month = int(ret[0][1])
                val = second_month - first_month + 1
                if (val < 0):
                    val += 12
                result += new_monthly_next(p, ret, val, ret_y) + " "
                key = 0
            else:
                result += new_monthly_next(p, ret, 1, ret_y) + " "


    result = delete_year_str(result)
    return result

def monthly_check_for_summary(prev, title):
    r = re.compile("(\D*)([\d,]*\d+)(월)(\D*)")
    q2 = re.compile("(\D*)([\d~]*\d+)(월)(\D*)")
    n = re.compile(("\d[ , ]+\d"))
    q = re.compile(("(\d*)~(\d*)"))
    y = re.compile("(\d*)(년)")
    # yy = re.compile('(\d*)( 년)')
    # yyy = re.compile('(\d*)(년 )')
    # only_y = re.compile('(\d+)(년)(분*)')
    c = re.compile("[']*(\d*)\.(\d*)\.(\d*)(\.)*")

    prev = delete_year_str(prev)
    title = delete_year_str(title)

    inc_month_value = 1
    if q.search(title):
        title_str = title.split(sep="~")
        # ~ 앞에나오는 문자열의 끝두자리(숫자부분)
        first_str = ""
        if title_str[0].strip()[-1] == "월":
            first_str = title_str[0].strip()[-3:-1]
        else:
            first_str = title_str[0].strip()[-2:]
        # ~ 뒤에 나오는 문자열의 앞 두자리(숫자부분)
        second_str = title_str[1].strip()[:2]

        if "0" <= first_str[1] <= "9":
            first_month = first_str[1]
            if "0" <= first_str[0] <= "9":
                first_month += first_str[0]
                first_month = first_str[::-1]
            first_month = int(first_month)

        if "0" <= second_str[0] <= "9":
            second_month = second_str[0]
            if "0" <= second_str[1] <= "9":
                second_month += second_str[1]
            second_month = int(second_month)

        inc_month_value = second_month - first_month + 1
        if(inc_month_value < 0):
            inc_month_value += 12


    # Key : 0 == 일반적인 케이스 / 1 == 연속된 달 / 2 == 분기
    l, key = 0, 0
    ret = []
    ret_y = []

    text_list = prev.split()
    pprev = ""

    result = ""

    for p in text_list:
        if c.search(p):
            f = c.findall(p)
            if len(f) == 2:
                date1 = datetime.datetime(int(f[0][0]), int(f[0][1]), int(f[0][2]))
                date2 = datetime.datetime(int(f[1][0]), int(f[1][1]), int(f[1][2]))
                if dateController.date2dateByDays(date1, date2) > 300:
                    # 1년 단위 차이라고 가정
                    # year_gap = dateController.date2dateByYears(date1,date2)
                    year_gap = round(dateController.date2dateByDays(date1, date2) / 365)
                    t = re.sub(
                        "[']*(\d*)\.(\d*)\.(\d*)(\.)*[~\-][']*(\d*)\.(\d*)\.(\d*)(\.)*",
                        dateController.jumpDateByYear(date1, year_gap)
                        + "~"
                        + dateController.jumpDateByYear(date2, year_gap),
                        p,
                    )
                    result += t + " "
                    # result += dateController.jumpDateByYear(date1,year_gap)+"~"+dateController.jumpDateByYear(date2,year_gap)
                elif dateController.date2dateByDays(date1, date2) > 31:
                    month_gap = round(dateController.date2dateByDays(date1, date2) / 31)
                    t = re.sub(
                        "[']*(\d*)\.(\d*)\.(\d*)(\.)*[~\-][']*(\d*)\.(\d*)\.(\d*)(\.)*",
                        dateController.jumpDateByMonth(date1, month_gap)
                        + "~"
                        + dateController.jumpDateByMonth(date2, month_gap),
                        p,
                    )
                    result += t + " "
            elif len(f) == 1:
                result += p + " "
        else:
            check = False
            # 년도가 등장하는 부분 시작
            if (y.match(pprev) and r.match(p)) or (y.match(pprev) and q2.match(p)):
                # print(pprev)
                temp = []
                m = l
                x = []
                while m < l + len(p):
                    if "0" <= prev[m] <= "9":
                        s = prev[m]
                        if "0" <= prev[m + 1] <= "9":
                            s += prev[m + 1]
                            m += 1
                        x.append(int(s))
                    m += 1
                for tmp in temp:
                    x.append(int(s))
                ret_y.append([int(pprev[:-1]), x])
                # year_part = pprev
                # 연도 붙이기
                # print("ret_y = " + str(ret_y))
            # 년도가 등장하는 부분 종료
            elif r.match(p) or q2.match(p) or q.match(p):
                temp = []
                m = l
                while m < l + len(p):
                    if "0" <= prev[m] <= "9":
                        s = prev[m]
                        if "0" <= prev[m + 1] <= "9":
                            s += prev[m + 1]
                            m += 1
                        temp.append(s)
                    m += 1
                ret.append(temp)

            l += len(p) + 1
            pprev = p
            # print(pprev)

        if not check:
            # print(p, ret_y)
            # print(p, ret)

            if q.search(p):
                key = 2
            if(key == 2):
                first_month = int(ret[0][0])
                second_month = int(ret[0][1])
                val = second_month - first_month + 1
                if (val < 0):
                    val += 12
                result += new_monthly_next(p, ret, val, ret_y) + " "
                key = 0
            else:
                result += new_monthly_next(p, ret, inc_month_value, ret_y) + " "


    result = delete_year_str(result)
    return result
def change_month(prev, to_month): # 특정 월호 날짜 변경
    r = re.compile("(\D*)([\d,]*\d+)(월)(\D*)")
    q2 = re.compile("(\D*)([\d~]*\d+)(월)(\D*)")
    n = re.compile(("\d[ , ]+\d"))
    q = re.compile(("~"))
    y = re.compile("(\d*)(년)")
    c = re.compile("[']*(\d*)\.(\d*)\.(\d*)(\.)*")

    prev = delete_year_str(prev) # 연도 제거

    # Key : 0 == 일반적인 케이스 / 1 == 연속된 달 / 2 == 분기
    l, key = 0, 0
    ret = []
    ret_y = []
    if n.search(prev):
        key = 1
    if q.search(prev):
        key = 2

    text_list = prev.split()
    pprev = ""

    result = ""

    for p in text_list:
        if c.search(p):
            f = c.findall(p)
            if len(f) == 2:
                date1 = datetime.datetime(int(f[0][0]), int(f[0][1]), int(f[0][2]))
                date2 = datetime.datetime(int(f[1][0]), int(f[1][1]), int(f[1][2]))
                if dateController.date2dateByDays(date1, date2) > 300:
                    # 1년 단위 차이라고 가정
                    # year_gap = dateController.date2dateByYears(date1,date2)
                    year_gap = round(dateController.date2dateByDays(date1, date2) / 365)
                    t = re.sub(
                        "[']*(\d*)\.(\d*)\.(\d*)(\.)*[~\-][']*(\d*)\.(\d*)\.(\d*)(\.)*",
                        dateController.jumpDateByYear(date1, year_gap)
                        + "~"
                        + dateController.jumpDateByYear(date2, year_gap),
                        p,
                    )
                    result += t + " "
                    # result += dateController.jumpDateByYear(date1,year_gap)+"~"+dateController.jumpDateByYear(date2,year_gap)
                elif dateController.date2dateByDays(date1, date2) > 31:
                    month_gap = round(dateController.date2dateByDays(date1, date2) / 31)
                    t = re.sub(
                        "[']*(\d*)\.(\d*)\.(\d*)(\.)*[~\-][']*(\d*)\.(\d*)\.(\d*)(\.)*",
                        dateController.jumpDateByMonth(date1, month_gap)
                        + "~"
                        + dateController.jumpDateByMonth(date2, month_gap),
                        p,
                    )
                    result += t + " "
            elif len(f) == 1:
                result += p + " "
        else:
            check = False
            # 년도가 등장하는 부분 시작
            if (y.match(pprev) and r.match(p)) or (y.match(pprev) and q2.match(p)):
                # print(pprev)
                temp = []
                m = l
                x = []
                while m < l + len(p):
                    if "0" <= prev[m] <= "9":
                        s = prev[m]
                        if "0" <= prev[m + 1] <= "9":
                            s += prev[m + 1]
                            m += 1
                        x.append(int(s))
                    m += 1
                for tmp in temp:
                    x.append(int(s))
                ret_y.append([int(pprev[:-1]), x])
                # year_part = pprev
                # 연도 붙이기
                # print("ret_y = " + str(ret_y))
            # 년도가 등장하는 부분 종료
            elif r.match(p) or q2.match(p):
                temp = []
                m = l
                while m < l + len(p):
                    if "0" <= prev[m] <= "9":
                        s = prev[m]
                        if "0" <= prev[m + 1] <= "9":
                            s += prev[m + 1]
                            m += 1
                        temp.append(s)
                    m += 1
                ret.append(temp)

            l += len(p) + 1
            pprev = p
            # print(pprev)

        if not check:
            # print(p, ret_y)
            # print(p, ret)
            result += change_month_to(p, ret, to_month) + " "

    result = delete_year_str(result)
    return result

def change_month_to(prev, month, to_month): # 특정 월로 텍스트를 변경
    cmonth = deepcopy(month)
    cmonth.sort(key=lambda x: int(x[0]))

    # 연도가 모두 없다고 가정
    for xi in range(len(cmonth) - 1, -1, -1):
        x = cmonth[xi]
        for i in range(len(x) - 1, -1, -1):
            if re.search(str(x[i]), prev):
                prev = re.sub(
                    "\A" + str(x[i]) + "월", "" + str(to_month) + "월", prev
                )
                prev = re.sub(
                    "~" + str(x[i]) + "월", "~" + str(to_month) + "월", prev
                )
                prev = re.sub(
                    "\(" + str(x[i]) + "월", "(" + str(to_month) + "월", prev
                )
                prev = re.sub(
                    "\(" + str(x[i]) + ",", "(" + str(to_month) + ",", prev
                )
                prev = re.sub(
                    "\A" + str(x[i]) + "월", "" + str(to_month) + "월", prev
                )
                prev = re.sub(
                    "\A" + str(x[i]) + ",", "" + str(to_month) + ",", prev
                )
                prev = re.sub(
                    "," + str(x[i]) + "월", "," + str(to_month) + "월", prev
                )
                prev = re.sub(
                    "," + str(x[i]) + ",", "," + str(to_month) + ",", prev
                )
    return prev


def new_monthly_next(prev, month, val, ymonth):
    cmonth = deepcopy(month)
    cmonth.sort(key=lambda x: int(x[0]))
    cymonth = deepcopy(ymonth)
    cymonth.sort(key=lambda x: int(x[0]))
    q = re.compile(("(\d*)~(\d*)"))

    # 1. 그냥 개별 월 ex) 3월, 4월 -> 5월, 6월
    #                   3,4월 -> 5,6월
    #                   3월 -> 4월
    # 2. 분기 ex) 4~6월 -> 7~9월
    #           4월~6월 -> 7월~9월
    #           4월 ~ 6월 (제대로 인식 안됨)
    #
    # 1번 연도가 개입하는 경우 -> ex) 2021년 11월, 12월 -> 2022년 1월, 2월
    # 2번 연도가 개입하는 경우 -> ex) 2021년 10월 ~ 12월 -> 2022년 1월 ~ 3월

    # 연도가 없음
    if len(cymonth) == 0:
        for xi in range(len(cmonth) - 1, -1, -1):
            x = cmonth[xi]
            next_months = month_inc(x, val)
            if q.search(prev):
                prev = re.sub(
                    str(x[0]) + "~" + str(x[1]) + "월",str(next_months[0]) +  "~" + next_months[1] + "월", prev
                )
                return prev

            for i in range(len(x) - 1, -1, -1):
                if re.search(str(x[i]), prev):
                    if int(next_months[i]) < 100:
                        prev = re.sub(
                            "\A" + str(x[i]) + "월", "" + next_months[i] + "월", prev
                        )
                        prev = re.sub(
                            "~" + str(x[i]) + "월", "~" + next_months[i] + "월", prev
                        )
                        prev = re.sub(
                            "\(" + str(x[i]) + "월", "(" + next_months[i] + "월", prev
                        )
                        prev = re.sub(
                            "\(" + str(x[i]) + ",", "(" + next_months[i] + ",", prev
                        )
                        prev = re.sub(
                            "\A" + str(x[i]) + "월", "" + next_months[i] + "월", prev
                        )
                        prev = re.sub(
                            "\A" + str(x[i]) + ",", "" + next_months[i] + ",", prev
                        )
                        prev = re.sub(
                            "," + str(x[i]) + "월", "," + next_months[i] + "월", prev
                        )
                        prev = re.sub(
                            "," + str(x[i]) + ",", "," + next_months[i] + ",", prev
                        )
                        # prev = re.sub(str(x[i])+",", next_months[i]+",", prev)
                        # prev = re.sub(str(x[i])+"~", next_months[i]+"~", prev)
                    else:
                        prev = re.sub(
                            "\A" + str(x[i]) + "월",
                            ""
                            + str(dateController.yearToday() + 1)
                            + "년 "
                            + str(int(next_months[i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "~" + str(x[i]) + "월",
                            "~"
                            + str(dateController.yearToday() + 1)
                            + "년 "
                            + str(int(next_months[i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "\(" + str(x[i]) + "월",
                            "("
                            + str(dateController.yearToday() + 1)
                            + "년 "
                            + str(int(next_months[i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "\(" + str(x[i]) + ",",
                            "("
                            + str(dateController.yearToday() + 1)
                            + "년 "
                            + str(int(next_months[i]) - 100)
                            + ",",
                            prev,
                        )
                        prev = re.sub(
                            "\A" + str(x[i]) + "월",
                            ""
                            + str(dateController.yearToday() + 1)
                            + "년 "
                            + str(int(next_months[i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "\A" + str(x[i]) + ",",
                            ""
                            + str(dateController.yearToday() + 1)
                            + "년 "
                            + str(int(next_months[i]) - 100)
                            + ",",
                            prev,
                        )
                        prev = re.sub(
                            "," + str(x[i]) + "월",
                            ","
                            + str(dateController.yearToday() + 1)
                            + "년 "
                            + str(int(next_months[i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "," + str(x[i]) + ",",
                            ","
                            + str(dateController.yearToday() + 1)
                            + "년 "
                            + str(int(next_months[i]) - 100)
                            + ",",
                            prev,
                        )
                        # prev = re.sub(str(x[i])+",", str(dateController.yearToday()+1)+"년 "+str(int(next_months[i])-100)+",", prev)
                        # prev = re.sub(str(x[i])+"~", str(dateController.yearToday()+1)+"년 "+str(int(next_months[i])-100)+"~", prev)

    # 연도가 있음
    else:
        next_months = []
        for x in cymonth:
            year = x[0]
            months = x[1]
            next_months.append(month_inc(months, val))
        # months.sort(reverse=True)
        # next_months.sort(reverse=True)

        for j in range(len(next_months) - 1, -1, -1):
            for i in range(len(cymonth[j][1])):
                if re.search(str(cymonth[j][1][i]), prev):
                    # prev = re.sub(str(cymonth[j][1][i]),next_months[j][i],prev)
                    if int(next_months[j][i]) < 100:
                        prev = re.sub(
                            "\A" + str(cymonth[j][1][i]) + "월",
                            "" + next_months[j][i] + "월",
                            prev,
                        )
                        prev = re.sub(
                            "~" + str(cymonth[j][1][i]) + "월",
                            "~" + next_months[j][i] + "월",
                            prev,
                        )
                        prev = re.sub(
                            "\(" + str(cymonth[j][1][i]) + "월",
                            "(" + next_months[j][i] + "월",
                            prev,
                        )
                        prev = re.sub(
                            "," + str(cymonth[j][1][i]) + "월",
                            "," + next_months[j][i] + "월",
                            prev,
                        )
                        prev = re.sub(
                            "\(" + str(cymonth[j][1][i]) + ",",
                            "(" + next_months[j][i] + ",",
                            prev,
                        )
                        prev = re.sub(
                            "," + str(cymonth[j][1][i]) + ",",
                            "," + next_months[j][i] + ",",
                            prev,
                        )
                        prev = re.sub(
                            "\A" + str(cymonth[j][1][i]) + "월",
                            "" + next_months[j][i] + "월",
                            prev,
                        )
                        prev = re.sub(
                            "\A" + str(cymonth[j][1][i]) + ",",
                            "" + next_months[j][i] + ",",
                            prev,
                        )
                        # prev = re.sub(str(cymonth[j][1][i])+",",next_months[j][i]+",",prev)
                        # prev = re.sub(str(cymonth[j][1][i])+"~",next_months[j][i]+"~",prev)
                    else:
                        # prev = re.sub(str(cymonth[j][0])+"년 ", "",prev)
                        prev = re.sub(
                            " " + str(cymonth[j][1][i]) + "월",
                            " "
                            + str(cymonth[j][0] + int(int(next_months[j][i]) / 100))
                            + "년 "
                            + str(int(next_months[j][i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "~" + str(cymonth[j][1][i]) + "월",
                            "~"
                            + str(cymonth[j][0] + int(int(next_months[j][i]) / 100))
                            + "년 "
                            + str(int(next_months[j][i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "\(" + str(cymonth[j][1][i]) + "월",
                            "("
                            + str(cymonth[j][0] + int(int(next_months[j][i]) / 100))
                            + "년 "
                            + str(int(next_months[j][i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "," + str(cymonth[j][1][i]) + "월",
                            ","
                            + str(cymonth[j][0] + int(int(next_months[j][i]) / 100))
                            + "년 "
                            + str(int(next_months[j][i]) - 100)
                            + "월",
                            prev,
                        )
                        prev = re.sub(
                            "\(" + str(cymonth[j][1][i]) + ",",
                            "("
                            + str(cymonth[j][0] + int(int(next_months[j][i]) / 100))
                            + "년 "
                            + str(int(next_months[j][i]) - 100)
                            + ",",
                            prev,
                        )
                        prev = re.sub(
                            "," + str(cymonth[j][1][i]) + ",",
                            ","
                            + str(cymonth[j][0] + int(int(next_months[j][i]) / 100))
                            + "년 "
                            + str(int(next_months[j][i]) - 100)
                            + ",",
                            prev,
                        )
                        # prev = re.sub(str(cymonth[j][1][i])+",", str(cymonth[j][0]+int(int(next_months[j][i]) / 100)) + "년 " + str(int(next_months[j][i]) - 100)+",", prev)
                        # prev = re.sub(str(cymonth[j][1][i])+"~", str(cymonth[j][0]+int(int(next_months[j][i]) / 100)) + "년 " + str(int(next_months[j][i]) - 100)+"~", prev)
                        # prev = re.sub(str(cmonth[i])," " + str(dateController.yearToday() + 1) + "년 " + str(int(next_months[i]) - 100),prev)
                # prev = re.sub(cymonth, next_months, prev)

                if int(next_months[j][0]) >= 100:
                    prev = re.sub(str(cymonth[j][0]) + "년 ", "", prev)

    return prev


if __name__ == "__main__":
    test_text = "테스트용(실습 2022년 12월) 지급"
    test2 = "12월"
    test3 = "2021 21년"
    test4 = "서울캠 경비용역 도급비(2022년 12월분)"
    test5 = "서울캠 경비용역 도급비(2022년도 12월분)"
    # test5 = "기능직2 직원 휴일 당직수당 지급(2022년12월분)"
    # test5 = "기능직2 직원 휴일 당직수당 지급(222222년 11월, 12월분)"

    # title[1] = monthly_check(title[1]).strip()
    # for i in range(len(res)):
    #     res[i] = monthly_check(res[i])

    print(change_month(test5, 5))
    # print(monthly_check(test2))
    # print(monthly_check(test3))
    print(monthly_check(test4))
    print(monthly_check(test5))

    # tax_date = ['2022-12-25']
    # tax_strpdate = datetime.strptime(tax_date[0], "%Y-%m-%d")
    # tax_strpdate = tax_strpdate + relativedelta(months=1)
    # tax_strpdate = datetime.strftime(tax_strpdate, "%Y-%m-%d")

    # sys.stdin = open(링크[3]+"_etc/errorCase.txt")
    # input()
    # while True:
    #     put = input()
    #     if put[0] == "<":
    #         break
    #     print("------------------")
    #     print(put,"->")
    #     result = monthly_check(put)
    #     print(result)
    #
    #     result = monthly_textReplace(result,"8")
    #     print(result)
