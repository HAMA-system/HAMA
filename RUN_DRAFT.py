import time

from linkData import *
from autoLogin import *
from alertController import *
from selenium.webdriver import ActionChains

def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

def draft(driver):
    driver.switch_to.frame(기안_프레임1)
    cpath(driver, 결재문서)
    time.sleep(3)
    driver.switch_to.default_content()
    driver.switch_to.frame(기안_프레임2)
    cpath(driver, 완료문서)
    time.sleep(1)
    while True:
        table = driver.find_element_by_id('DocList')
        print()
        i = 1
        for tr in table.find_elements(by=By.TAG_NAME, value="tr")[1:]:
            print("번호 ",i," : ",sep='',end='\t')
            for td in tr.find_elements(by=By.TAG_NAME, value="td")[1:]:
                print(td.get_attribute("innerText"),end='\t')
            print()
            i += 1
        print("\n인쇄를 할 문서들의 시작번호와 끝번호를 입력해주세요. ex) 1 20")
        print("혹은 이동할 페이지 번호를 입력해주세요. ex) 2")
        inp = list(map(int,input().split()))
        if len(inp) == 2:
            start, end = inp[0], inp[1]
        elif len(inp) == 1:
            page = 페이지_변경[:29] + str(inp[0]+2) + 페이지_변경[30:]
            cpath(driver, page)
            time.sleep(1)
            continue
        for i in range(start, end+1):

            # 시작할 때, 반복할 때 주소가 달라야 클릭이 됨
            if i == start:
                num = 문서번호1[:64] + str(i) + 문서번호1[65:]
            else:
                num = 문서번호2[:67] + str(i) + 문서번호2[68:]

            print(i,"번 문서 인쇄중...",sep='')
            cpath(driver, num)
            time.sleep(3)
            cpath(driver, 인쇄)
            time.sleep(1)
            driver.switch_to.frame(인쇄_프레임)
            cpath(driver, 문서인쇄)
            time.sleep(10)

            # ** shadow-root 같은 element는 find_element(by=) 이용해야함 **
            driver.switch_to.window(driver.window_handles[1])
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
            driver.switch_to.frame(인쇄_프레임)
            cpath(driver, 인쇄_창닫기)
            driver.switch_to.parent_frame()
            cpath(driver, 기안_창닫기)

        print("모든 문서 출력이 완료되었습니다.")