# import threading
import time
from ESSENTIAL_FILES import manage
from EXECUTION_FILE import RUN_DRAFT

timer = 0

def startTimer():
    global timer
    while True:
        time.sleep(1)
        timer += 1
        # print(timer)
        # if timer > 60 * 20 and manage.sema == 0:
        if timer > 60 * 20 :
            timer = 0
            # manage.refresh()
            RUN_DRAFT.refresh()
            print("자동 로그아웃 방지중입니다.")


    # timer = threading.Timer(5, startTimer)
    # timer.start()


