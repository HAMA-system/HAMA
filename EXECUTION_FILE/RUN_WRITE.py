from selenium import webdriver
from FUNC_LIBRARY import errorController, autoLogin
from ESSENTIAL_FILES import manage
from HIDDEN_FILES import linkData

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
    f1 = float(6365000)
    f2 = float(636500)
    f3 = float(6365)

    print("{:.0f}".format(float(6365000)))
    print("{:.0f}".format(float("6365000")))
    print(str(f2))
    print(f3)

