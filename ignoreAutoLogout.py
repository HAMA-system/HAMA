import threading

def startTimer():
    timer = threading.Timer(5, startTimer)
    timer.start()


    print("자동로그아웃 방지를 위해 다시 로그인하는 중입니다.")