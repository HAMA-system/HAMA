import os
import re
import time
import unicodedata

from xlsxFileController import get_all_directory_info
from linkData import 링크
from manage import monthly_textReplace

def replace():
    info = get_all_directory_info()
    autoFolder = os.listdir(링크[3])
    autoPath = 링크[3]
    inPath = 링크[3] + "in/"
    outPath = 링크[3] + "결의서 작성 필요/"
    # outFoler 나중에

    print("파일 배치를 시작합니다.")

    # out 폴더 있는지 체크
    if '결의서 작성 필요' not in autoFolder:
        os.mkdir(링크[3] + '결의서 작성 필요')
    if '기안 필요' not in autoFolder:
        os.mkdir(링크[3] + '기안 필요')

    # for new in info:
    for num, keyword, month, title in info:
        if num == -1:
            continue
        if title != '_':
            if month != '_' and month != -1 and month is not None:
                print(title, month)
                title = monthly_textReplace(title, str(month)).strip()
            fileName = title + "#" + keyword
            if fileName not in os.listdir(outPath):
                os.mkdir(outPath + fileName)

    outFolder = os.listdir(outPath)

    # Folder에서 Keyword 뽑아서 Sort 및 Title Mapping
    keywordList = []
    keyToFileName = dict()
    for fileName in outFolder:
        keyword = fileName.split('#')[-1]
        keywordList.append(keyword)
        keyToFileName[keyword] = fileName

    keywordList = sorted(keywordList, key=len, reverse=True)

    print("\n더 이상 옮길 파일이 없습니다.\n\n[ 옮겨진 파일 ]")
    for keyword in keywordList:
        for inFile in os.listdir(inPath):
            if re.search(unicodedata.normalize('NFC', keyword.replace(" ", "")), unicodedata.normalize('NFC', inFile.replace(" ", ""))):
                print("(", inFile, ") 파일을", "-> (", keyToFileName[keyword], ") 폴더로 옮겼습니다")
                os.replace(inPath + inFile, outPath + keyToFileName[keyword] + "/" + inFile)

    print("\n[ 옮겨지지 않은 파일 ]\n- ",end='')
    print(*sorted(os.listdir(inPath)),sep='\n- ')
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


if __name__ == '__main__':
    r = True
    while r:
        replace()
        print("\n한번 더 파일을 옮기시겠습니까? 1(예)/2(종료)")
        while True:
            put = input()
            if put == '1':
                break
            elif put == '2':
                r = False
                break
            else:
                print("잘못된 입력입니다.")