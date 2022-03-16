def errorMsg(errNum):
    errDic = {0 : "크롬 드라이버 버전 오류", 1 : "파일을 찾을 수 없음", 2 : "첫 셀과 마지막 셀이 같은 행에 있지 않음"}

    print(errDic.get(errNum))
