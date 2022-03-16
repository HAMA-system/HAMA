
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

    # firstcell = 'B4'
    # lastcell = 'F4'
    #
    # print(firstcell[1:])
    # print(chr(ord(lastcell[:1])+1)+firstcell[1:])
    print(data)

    data2 = xlsxFileController.get_singleline_data(file,'Sheet1','B4','G4')
    print(data2)
    print('h')
