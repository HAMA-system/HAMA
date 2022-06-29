import os
import re

from xlsxFileController import get_all_directory_info
from linkData import 링크

def replace():
    print("파일 이동을 시작합니다.")
    info = get_all_directory_info()
    path = 링크[3] + "in/"
    dpath = 링크[3] + "out/"

    # out 폴더 있는지 체크
    isOut = False
    for f in os.listdir(링크[3]):
        if f == 'out':
            isOut = True
            break
    if not isOut:
        os.mkdir(링크[3] + 'out')

    # 폴더 생성
    for new in info:
        for num, keyword in new:
            if num == -1:
                continue
            folder = str(num) + " " + keyword
            if folder not in os.listdir(dpath):
                os.mkdir(dpath + folder)


    # TODO
    #   CASE 1)
    #       복사
    #       복사점
    #       복사.pdf
    #       복사점.pdf
    #   CASE 2)
    #       신한은행 도급비
    #       신한은행 임대료
    #       신한은행

    # 파일 이동
    folder = []
    file = []
    print("\n파일 이동이 완료되었습니다.\n\n이동된 파일")
    outDir = sorted(os.listdir(dpath),key=lambda x:len("".join(x.split()[1:])),reverse=True)
    for fd in outDir:
        fd_str = "".join(fd.split()[1:])
        for f in os.listdir(path):
            f_str = "".join(f.split())
            if re.search(fd_str, f_str):
                print("\n<", f, "> 파일을", "\n-> [", fd, "] 폴더로 이동하였습니다")
                os.replace(path+f, dpath+fd+'/'+f)
    print("\n남아있는 파일")
    for f in os.listdir(path):
        print("-",f)

if __name__ == '__main__':
    r = True
    while r:
        replace()
        print("\n파일을 이동하시겠습니까? 1(예)/2(종료)")
        while True:
            put = input()
            if put == '1':
                break
            elif put == '2':
                r = False
                break
            else:
                print("잘못된 입력입니다.")