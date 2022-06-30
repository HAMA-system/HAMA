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
    # for new in info:
    for num, keyword in info:
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
    #       폴더 이름 결의서 제목으로 하기 ?


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