from selenium import webdriver
import xlsxFileController
import errorController
import autoLogin
import time

def set_chromedriver():
    try:
        driver = webdriver.Chrome("./chromedriver")
    except:
        errorController.errorMsg(0)
    return driver

if __name__ == '__main__':
    driver = set_chromedriver()
    driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
    driver = autoLogin.login(driver)
    while True:
        print("원하시는 서비스를 입력하세요. (조회/작성/종료)")
        select = input()
        if select == '조회':
            autoLogin.cpath(driver,
                  '/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/ul/li[2]/span/a')
        elif select == '작성':
            autoLogin.cpath(driver,'/html/body/form/div[3]/div[1]/div/div[1]/ul/li[2]/ul/li/ul/li/ul/li[2]/ul/li[2]/ul/li[1]/span/a')
        elif select == '종료':
            break
    # file = xlsxFileController.load_xls('example.xlsx')
    # data = xlsxFileController.get_cell_data(file, 'Sheet1', 'B4')
    #
    # print(data)
    #
    # data2 = xlsxFileController.get_singleline_data(file,'Sheet1','B4','G4')
    # print(data2)
    # print('h')
