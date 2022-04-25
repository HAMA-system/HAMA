def dismiss(driver):
    while True:
        try:
            driver.switch_to.alert.dismiss()
            break
        except:
            pass


def accept(driver):
    while True:
        try:
            driver.switch_to.alert.accept()
            break
        except:
            pass