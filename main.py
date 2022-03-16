
from selenium import webdriver
import xlsxFileController

def set_chromedriver():
    try:
        driver = webdriver.Chrome("/Users/han/hans/workspace/kwanjae/chromedriver")
    except:
        print('chrome driver version error')
    url = 'https://ngw.hongik.ac.kr/myoffice/ezportal/index_portal.aspx'
    driver.get(url)




if __name__ == '__main__':
    # set_chromedriver()
    file = xlsxFileController.load_xls('example.xlsx')
    data = xlsxFileController.get_cell_data(file, 'Sheet1', 'B4')
    print(data)
    print('h')
