from selenium import webdriver
from FUNC_LIBRARY import errorController, autoLogin, xlsxFileController
from ESSENTIAL_FILES import manage
from HIDDEN_FILES import linkData
from HIDDEN_FILES.linkData import 링크


def set_chromedriver():
    try:
        # driver = webdriver.Chrome("./chromedriver.exe")
        # driver = webdriver.Chrome("C:/auto/chromedriver.exe")
        # driver = webdriver.Chrome("/Users/han/hans/workspace/kwanjae/chromedriver")
        driver = webdriver.Chrome(linkData.링크[0])
        # driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/chromedriver")
        # driver = webdriver.Chrome("/Users/MS/PycharmProjects/HAMA/dist/chromedriver")

    except:
        errorController.errorMsg(0)
    return driver


# driver = set_chromedriver()
# driver.get("https://www.hongik.ac.kr/login.do?Refer=https://ngw.hongik.ac.kr/login_hongik.aspx")
# driver = autoLogin.login(driver)
#
# manage.write(driver)

if __name__ == '__main__':
    # f1 = str(6364999.9999999)
    # f2 = str(636500)
    # f3 = float(6365)
    #
    # print(round(int(f1)))
    # print(round(float(str(f1))))
    # print(str(f2))
    # print(f3)

    file = xlsxFileController.load_xls(링크[2])
    input_data = xlsxFileController.all_data_fetch(file, "결의내역", "E15", "X15")
    target_data = input_data
    print(str(target_data[9][16]))
    print(type(target_data[9][16]))
    print(str(target_data[9][17]))
    print(type(target_data[9][17]))
    print(target_data[9][18])
    print(type(target_data[9][18]))

    print(str(target_data[10][16]))
    print(type(target_data[10][16]))
    print(str(target_data[10][17]))
    print(type(target_data[10][17]))
    print(target_data[10][18])
    print(type(target_data[10][18]))