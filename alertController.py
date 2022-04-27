def dismissAlert(driver):
    while True:
        try:
            driver.switch_to.alert.dismiss()
            break
        except:
            pass


def acceptAlert(driver):
    while True:
        try:
            driver.switch_to.alert.accept()
            break
        except:
            pass