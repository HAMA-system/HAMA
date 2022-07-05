import os
import re
import time

from xlsxFileController import get_all_directory_info
from linkData import 링크

def replace():
    info = get_all_directory_info()
    autoFolder = os.listdir(링크[3])
    autoPath = 링크[3]
    inPath = 링크[3] + "in/"
    inFolder = os.listdir()
    outPath = 링크[3] + "결의서 작성 필요/"

    print("파일 이동을 시작합니다.")

    # out 폴더 있는지 체크
    if '결의서 작성 필요' not in autoFolder:
        os.mkdir(링크[3] + '결의서 작성 필요')
    if '기안 필요' not in autoFolder:
        os.mkdir(링크[3] + '기안 필요')

    # for new in info:
    for num, keyword, _, title in info:
        if num == -1:
            continue
        if title != '_':
            fileName = title + "#" + keyword
            if fileName not in os.listdir(outPath):
                os.mkdir(dpath + fileName)

    outFolder = os.listdir(outPath)

    # Folder에서 Keyword 뽑아서 Sort 및 Title Mapping
    keywordList = []
    keyToFileName = dict()
    for fileName in outFolder:
        keyword = fileName.split('#')[-1]
        keywordList.append(keyword)
        keyToFileName[keyword] = fileName

    keywordList = sorted(keywordList, key=len, reverse=True)

    print("\n파일 이동이 완료되었습니다.\n\n이동된 파일")
    for keyword in keywordList:
        for inFile in inFolder


    for fd_key in outDir:
        # fd_str = "".join(fd.split()[1:])
        # fd_str = title_key[fd]
        fd_title = key_title[fd_key]
        for f in os.listdir(path):
            f_str = "".join(f.split())
            f_key = "".join(fd_key.split())
            print(f_key,f_str,re.search(f_key, f_str))
            if re.search(f_key, f_str):
                print("\n<", f, "> 파일을", "\n-> [", fd_title, "] 폴더로 이동하였습니다")
                os.replace(path+f, dpath+fd_title+'/'+f)
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