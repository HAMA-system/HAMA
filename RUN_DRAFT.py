import time

from linkData import *
from autoLogin import *
from alertController import *
def draft(driver):
    driver.switch_to.frame(기안_프레임1)
    cpath(driver, 결재문서)
    time.sleep(3)
    driver.switch_to.default_content()
    driver.switch_to.frame(기안_프레임2)
    cpath(driver, 완료문서)
    table = driver.find_element_by_id('DocList')
    print()
    i = 0
    for tr in table.find_elements(by=By.TAG_NAME, value="tr")[1:]:
        print("번호 ",i," : ",sep='',end='\t')
        for td in tr.find_elements(by=By.TAG_NAME, value="td")[1:]:
            print(td.get_attribute("innerText"),end='\t')
        print()
        i += 1
    time.sleep(10000)