
from selenium import webdriver
import xlsxFileController
import errorController

def set_chromedriver():
    try:
        driver = webdriver.Chrome("/Users/han/hans/workspace/kwanjae/chromedriver")
    except:
        errorController.errorMsg(0)
    return driver


if __name__ == '__main__':
    driver = set_chromedriver()
    driver.get('https://ngw.hongik.ac.kr/myoffice/ezportal/index_portal.aspx')

    file = xlsxFileContro가ller.load_xls('example.xlsx')
    data = xlsxFileController.get_cell_data(file, 'Sheet1', 'B4')

    print(data)

    data2 = xlsxFileController.get_singleline_data(file,'Sheet1','B4','G4')
    print(data2)
    print('h')
