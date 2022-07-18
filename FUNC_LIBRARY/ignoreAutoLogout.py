# import threading
import time
from ESSENTIAL_FILES import manage

timer = 0

def startTimer():
    global timer
    while True:
        time.sleep(1)
        timer += 1
        if timer > 60 * 20 and manage.sema == 0:
            timer = 0
            manage.refresh()
            print("자동 로그아웃 방지중입니다.")


    # timer = threading.Timer(5, startTimer)
    # timer.start()


