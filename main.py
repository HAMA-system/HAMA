from selenium import webdriver
import xlsxFileController
import dateController
import errorController
import autoLogin
import manage


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
            manage.lookup(driver)
        elif select == '작성':
            manage.write(driver)
        elif select == '종료':
            break
    # print(dateController.date1year())

    # file = xlsxFileController.load_xls('example.xlsx')
    # data = xlsxFileController.get_cell_data(file, 'Sheet1', 'B4')
    #
    # print(data)
    #
    # data2 = xlsxFileController.get_singleline_data(file,'Sheet1','B4','G4')
    # print(data2)
    # print('h')
