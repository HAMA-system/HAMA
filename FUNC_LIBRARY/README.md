##  KorStringRecognizer.py
* 프로그램 내부에서 osdir을 통해 읽어들인 파일명과 하드코딩한 문자열이 동일하지 않는 오류가 발생하여 해결한 파일
* 읽어들인 파일명이 "ㅍㅏㅇㅣㄹ"과 같이 자모가 분리되어 유니코드로 입력 받기 때문에 인코딩해주어야 함
* 최초에는 함수로 구현했으나 간단하게 해결 가능하여 해당 파일 내 main 함수를 참고하면 별도의 절차 없이 한글 인코딩이 가능함
	 
##  dateController.py
* 날짜 형식을 원하는 형태로 수정하기 위한 파일
* 사용 예시는 파일 내 main 함수를 참조

##  errorController.py
* 프로그램 내에서 발생하는 다양한 오류 사항을 메시지로 정리해놓는 파일
* 현재는 xlsxFileController 등에서만 사용되고 많이 사용하지 않았음
	 
##  xlsxFileController.py
* 엑셀 파일을 읽어오고 자료구조에 정리하기 위한 파일
* 셀 하나의 입력, 한 행 입력, 한 열 입력 등 필요한 대부분의 기능이 구현되어 있음
	 
##  help.py
* 사용자에게 제공되는 도움말
* 구현은 완료되어 있으나 현재는 실행파일에 포함되지 않았음
 
##  help.txt
* help.py 파일에서 읽어들이는 텍스트 파일
* 긴 길이의 도움말을 텍스트 파일에서 작성하도록 하였음
* <a>와 </a>의 형태로 문자열을 구별하여 읽어들임

##  alertController.py
* selenium 작동 중 팝업 알림창으로 인한 오류를 잡기 위해 닫거나 확인을 누르도록 구현

##  autoLogin.py
* selenium을 이용한 chromedriver로 회계시스템에 로그인을 수행
* 사용되는 로그인 아이디와 패스워드는 loginData.xlsx에서 작성
* driver 객체와 xpath, id 또는 name 값을 넘겨서 웹 내 특정 오브젝트를 클릭하거나 텍스트를 입력하는 일을 수행하는 함수가 포함되어 있음

##  ignoreAutoLogout.py
* 회계 시스템에 로그인한 채 장시간 방치할 때 자동 로그아웃이 되지 않도록 방지하는 파일
