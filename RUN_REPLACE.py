import os
import re
import time

from xlsxFileController import get_all_directory_info
from linkData import 링크

def replace():
    print("파일 이동을 시작합니다.")
    info = get_all_directory_info()
    path = 링크[3] + "in/"
    dpath = 링크[3] + "결의서 작성 필요/"

    # out 폴더 있는지 체크
    isOut = False
    isDraft = False
    for f in os.listdir(링크[3]):
        if f == '결의서 작성 필요':
            isOut = True
        if f == '기안 필요':
            isDraft = True
    if not isOut:
        os.mkdir(링크[3] + '결의서 작성 필요')
    if not isDraft:
        os.mkdir(링크[3] + '기안 필요')
    # 폴더 생성
    # for new in info:
    title_key = dict()
    key_title = dict()
    for num, keyword, _, title in info:
        if num == -1:
            continue
        if title != '_':
            title_key[title] = keyword
            key_title[keyword] = title
            # folder = str(num) + " " + keyword
            folder = title
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
    #   CASE 3)
    #       2022학년도 후기 대학원 입시 구술시험장 준비 및 정...
    #       봉사학생 근무확인표 및 개인정보수집 동의서.pdf
    #       간식대 영수증.pdf
    #   해결방안)
    #       다른 결의서와 키워드가 겹칠 수 있을 때 :
    #           최대한 길게 키워드 잡기.
    #           그럼에도 겹칠 경우 ????
    #           한번에 replace 하지 말고 여러번 나눠서 ?
    #       파일마다 중복되는 키워드 없는 경우 :
    #           직접 올리는 수밖에 없음.
    #           다른 키워드에 들어가면 문제
    #   개선사항)
    #       결재필요 폴더, 결재완료 폴더 생성하기 ?
    #       만약 파일이 없으면 폴더 생성 X <- 웬만하면 파일 있어서 필요한가?
    #   결의서 제목으로 Replace 하면 키워드 하나만 써도 됨
    #   정기내역 추가 해야함
    # 파일 이동
    folder = []
    file = []
    print("\n파일 이동이 완료되었습니다.\n\n이동된 파일")
    # outDir = sorted(os.listdir(dpath),key=lambda x:len("".join(x.split()[1:])),reverse=True)
    outDir = os.listdir(dpath)
    for i, x in enumerate(outDir):
        print(title_key,x)
        outDir[i] = title_key[x]
    outDir = sorted(outDir, key=len, reverse=True)
    # print(outDir)
    # time.sleep(10000)
    for fd_key in outDir:
        # fd_str = "".join(fd.split()[1:])
        # fd_str = title_key[fd]
        fd_title = key_title[fd_key]
        for f in os.listdir(path):
            f_str = "".join(f.split())
            if re.search("".join(fd_key.split()), f_str):
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