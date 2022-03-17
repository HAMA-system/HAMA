from selenium import webdriver
import xlsxFileController
import errorController
import autoLogin

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
    file = xlsxFileController.load_xls('example.xlsx')
    data = xlsxFileController.get_cell_data(file, 'Sheet1', 'B4')

    print(data)

    data2 = xlsxFileController.get_singleline_data(file,'Sheet1','B4','G4')
    print(data2)
    print('h')
