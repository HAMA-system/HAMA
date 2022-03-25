import time
import dateController
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from autoLogin import *
from linkData import *
import xlsxFileController


def lookup(driver):
    driver.switch_to.default_content()
    time.sleep(1)
    cpath(driver,결의서_조회)
    driver.switch_to.frame(조회_프레임)
    while True:

        while True:
            print("회계 구분번호를 입력해주세요. ex) 1(등록금)/2(비등록금) ")
                # acc, res = map(str,input().split())
            acc = input().strip()
            if acc == '1' or acc == '2':
                break
            print("잘못된 입력입니다.")

        while True:
            print("결의서 구분번호를 입력해주세요. ex) 1(전체)/2(수입)/3(지출)/4(대체)")
            res = input().strip()
            if res == '1' or res == '2' or res == '3' or res == '4':
                break
            print("잘못된 입력입니다.")

        while True:
            print("원하시는 기간을 선택하세요. ex) 1/3/6/12/2022)")
            month = input().strip()
            if len(month) == 1 or len(month) == 2 or len(month) == 4:
                break
            print("잘못된 입력입니다.")

        if len(month) == 4:
            fname(driver,'txtSAcctYear',month)
        else:
            fname(driver,'txtSAcctYear','2021')
        select = Select(driver.find_element_by_xpath(회계구분_조회))
        if acc == '1':
            select.select_by_index(0)
        elif acc == '2':
            select.select_by_index(1)

        select = Select(driver.find_element_by_xpath(결의서구분))
        if res == '1':
            select.select_by_index(1)
        elif res == '2':
            select.select_by_index(1)
        elif res == '3':
            select.select_by_index(2)
        elif res == '4':
            select.select_by_index(3)

        if month == '1':
            fname(driver,'DpFrDt',dateController.date1month())
        elif month == '3':
            fname(driver,'DpFrDt',dateController.date3month())
        elif month == '6':
            fname(driver,'DpFrDt',dateController.date6month())
        elif month == '12':
            fname(driver,'DpFrDt',dateController.date1year())
        elif len(month) == 4:
            fname(driver,'DpFrDt',month+'0301')
            fname(driver,'DpToDt',str(int(month)+1)+'0228')

        elif month == '종료':
            break
        else:
            print("잘못된 입력입니다.")
        if len(month) != 4:
            fname(driver,'DpToDt',dateController.dateToday())
        cname(driver,'CSMenuButton1$List')
        print("--------------------------------------------")
def write(driver):

    # TODO
    #   지급처 추가
    #   엑셀의 없음을 빈 칸으로 변경 (편의성)
    #   해결할 것 :
    #   - 세금이 자동으로 뜨는 것 과 다를 때(버스임대) <- 버스같은 경우 톨비는 세금이 안나와서 세금 되는 금액만 포함
    #   - 증빙세금 8개인데 세금탭에는 2개 <- 관리비 임대료 묶어서 부가세 포함 4개가 1세트
    #   => 구조 변경 방법 생각 해 봐야 할듯
    #   일단 세금계산서도 다 작성 하는걸로 하고 고칠 수 있으면 고치는걸로





    driver.switch_to.default_content()
    cpath(driver,결의서_작성)
    driver.switch_to.frame(작성_프레임)

    input_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('data.xlsx'),'결의내역','A3','R3')
    # print(len(input_data))
    # TODO
    # prev = input_data[0][0]
    for i in range(len(input_data)):
        print(i+3,'행 입력중입니다.',sep='')
        # TODO
        # if prev != input_data[i][0]:
        #   cpath(driver,제출)
        #   time.sleep(3)
        select = Select(driver.find_element_by_xpath(회계구분_작성))
        if input_data[i][1] == '등록금':
            select.select_by_index(0)
        elif input_data[i][1] == '비등록금':
            select.select_by_index(1)


        # print(1)
        # time.sleep(1)
        select = Select(driver.find_element_by_id('ddlResolutionDiv'))
        # print(2)
        # time.sleep(1)
        if input_data[i][2] == '수입결의서':
            select.select_by_index(0)
        elif input_data[i][2] == '지출결의서':
            select.select_by_index(1)
        # print(2.5)
        # time.sleep(5) # !!!!!!!!!!
        time.sleep(1)
        fpath(driver,사업코드,input_data[i][1])
        # time.sleep(2)
        # print(3)
        epath(driver,사업코드)
        # print(3.5)
        # time.sleep(1) # !!!!!!!!!!
        driver.switch_to.frame('frmPopup')
        # time.sleep(1)
        # print(4)
        epath(driver,사업팝업)
        driver.switch_to.default_content()
        driver.switch_to.frame('ifr_d4_AHG020P')
        fpath(driver,계정과목,input_data[i][4])
        epath(driver,계정과목)
        if input_data[i][5] is not None:
            fpath(driver,관리코드,input_data[i][5])
            epath(driver,관리코드)
            driver.switch_to.frame('frmPopup')
            epath(driver,관리팝업)
            driver.switch_to.default_content()
            driver.switch_to.frame('ifr_d4_AHG020P')
        fpath(driver,예산부서,input_data[i][8])
        select = Select(driver.find_element_by_id('ddlDetailEvidenceGb'))

        if input_data[i][9] == '없음':
            select.select_by_index(0)
        elif input_data[i][9] == '세금':
            select.select_by_index(1)
        elif input_data[i][9] == '기타':
            select.select_by_index(2)
        elif input_data[i][9] == '영수증':
            select.select_by_index(3)

        if input_data[i][12] is not None:
            fpath(driver,지출,input_data[i][12])
        if input_data[i][13] is not None:
            fpath(driver,수입,input_data[i][13])
        fpath(driver,적요,input_data[i][14])
        cpath(driver,결의내역_제출)

        if input_data[i][9] == '세금':
            time.sleep(0.3)
            driver.switch_to.alert.dismiss()

        # TODO
        #   세금 계산서 마지막에 한번에 해야함 구조 변경 필요
        #   위의 prev 조건문 안에 넣으면 될 듯

        '''
        if input_data[i][9] == '세금':
            time.sleep(1)
            driver.switch_to.alert.accept()


            # for j 돌려서 결의내역 A값과 같은 것 찾음
            tax_data = xlsxFileController.all_data_fetch(xlsxFileController.load_xls('data.xlsx'), '세금계산', 'A3', 'J3')
            for j in range(len(tax_data)):
                if tax_data[j][0] == input_data[i][0]:
                    break

            # print(tax_data)
            fpath(driver,발행일자,tax_data[j][2].strftime("%Y%m%d"))
            epath(driver,발행일자)
            select = Select(driver.find_element_by_id('ddlBillDiv'))
            if tax_data[j][6] == '일반':
                select.select_by_index(1)
            elif tax_data[j][6] == '전자':
                select.select_by_index(2)
            elif tax_data[j][6] == '영수증':
                select.select_by_index(3)

            # TODO 거래처 고르는 것 어떡할 지 생각. tax[][2]
            fpath(driver,거래처,'')
            epath(driver,거래처)
            time.sleep(1) # 없어도 돌아가긴 함

            driver.switch_to.frame('frmPopup')

            fpath(driver,사업자번호,tax_data[j][3])
            epath(driver,사업자번호)
            driver.switch_to.default_content()
            driver.switch_to.frame('ifr_d4_AHG020P')
            # TODO 공급가액은 지출일때만 자동 (수입은 세금 없는 것 같음)
            cpath(driver,세금계산_제출)
            time.sleep(2)
            cpath(driver,결의내역_탭)
        time.sleep(1)
        '''
        # prev = input_data[i][0]


    print("입력이 완료되었습니다.")
    time.sleep(10000)

