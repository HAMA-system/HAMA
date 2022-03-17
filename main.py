from selenium import webdriver
import xlsxFileController
import errorController

#test
def set_chromedriver():
    try:
        driver = webdriver.Chrome("./chromedriver")
    except:
        errorController.errorMsg(0)
    return driver

if __name__ == '__main__':
    driver = set_chromedriver()
    driver.get('https://itss.hongik.ac.kr/GateWeb/index.aspx#')
    
    file = xlsxFileController.load_xls('example.xlsx')
    data = xlsxFileController.get_cell_data(file, 'Sheet1', 'B4')

    print(data)

    data2 = xlsxFileController.get_singleline_data(file,'Sheet1','B4','G4')
    print(data2)
    print('h')
