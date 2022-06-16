import os
import re
from xlsxFileController import get_all_directory_info
from linkData import 링크

def replace():
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
            folder = str(num) + " " + keyword
            if folder not in os.listdir(dpath):
                os.mkdir(dpath + folder)

    # 파일 이동
    folder = []
    file = []
    print("\n파일 이동이 완료되었습니다.\n\n이동된 파일")
    for fd in os.listdir(dpath):
        fd_str = "".join(fd.split()[1:])
        for f in os.listdir(path):
            f_str = "".join(f.split())

            if re.search(fd_str, f_str):
                print("-",f)
                os.replace(path+f, dpath+fd+'/'+f)
    print("\n남아있는 파일")
    for f in os.listdir(path):
        print("-",f)

if __name__ == '__main__':
    replace()