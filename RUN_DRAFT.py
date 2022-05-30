import time
import pyautogui

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
    table = driver.find_element_by_id('DocList')
    print()
    i = 1
    for tr in table.find_elements(by=By.TAG_NAME, value="tr")[1:]:
        print("번호 ",i," : ",sep='',end='\t')
        for td in tr.find_elements(by=By.TAG_NAME, value="td")[1:]:
            print(td.get_attribute("innerText"),end='\t')
        print()
        i += 1
    print("\n인쇄를 할 문서들의 시작번호와 끝번호를 입력해주세요.")
    start, end = map(int,input().split())
    for i in range(start, end+1):
        num = 문서번호[:64] + str(i) + 문서번호[65:]
        print(i,"번 문서 인쇄중...",sep='')
        cpath(driver, num)
        time.sleep(3)
        cpath(driver, 인쇄)
        time.sleep(1)
        driver.switch_to.frame('Main_iFrameLayer')
        cpath(driver, 문서인쇄)

        time.sleep(10)
        # ** shadow-root 같은 element는 find_element(by=) 이용해야함 **
        driver.switch_to.window(driver.window_handles[1])
        r0 = driver.find_element(by=By.TAG_NAME, value=섀도0)
        sr0 = expand_shadow_element(driver, r0)
        r1 = sr0.find_element(by=By.TAG_NAME,value=섀도1)
        sr1 = expand_shadow_element(driver, r1)
        r2 = sr1.find_element(by=By.TAG_NAME,value=섀도2)
        sr2 = expand_shadow_element(driver, r2)
        save = sr2.find_element(by=By.CLASS_NAME,value=인쇄확인)
        # save.click()
        print(0)
        # 테스트용 인풋
        input()
        print(1)
        driver.switch_to.window(driver.window_handles[0])
        print(2)
        # driver.switch_to.default_content()
        # driver.switch_to.frame(기안_프레임2)
        # TODO
        #   창닫기 안돼서 반복작업 안됨. 고쳐야 함
        cpath(driver, 인쇄_창닫기)
        cpath(driver, 기안_창닫기)
        print(3)