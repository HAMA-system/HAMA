# HAMA
Hongik Accounting Management Advanced System

## Project Info

## Files
* RUN_LOOKUP.py
  * 기간, 결의서 내용 등으로 편리하게 결의서 검색하기 위한 실행파일
  
* RUN_REPLACE.py
  * 결의서 첨부파일을 키워드에 맞게 폴더로 분류해주기 위한 실행파일
  
* RUN_WRITE.py
  * data.xlsx 파일을 읽어들여 자동으로 결의서를 작성하기 위한 실행파일
  
* RUN_DRAFT.py
  * 기안 작성을 위한 실행파일
  
 
* ~~RUN_MODIFY.py~~
  * ~~결의서 수정을 위한 실행파일~~
  * RUN_DRAFT와 합쳐졌음 (07.13)
  
* _icon_
  * Lookup, Modify, Write, Draft, Replace 등 실행파일에 사용될 아이콘 파일들
  
* _ttest_
  * Replace 테스트를 위한 임시 폴더
  
* .DS_Store
  * Mac 환경에서 자동으로 생성되는 파일로 삭제해도 되는 파일
  
* .gitignore
  * 공개하지 않는 파일과 디바이스 별 다른 파일 등이 git에 올라가지 않도록 작성됨
  
* KorStringRecognizer.py
  * 프로그램 내부에서 osdir을 통해 읽어들인 파일명과 하드코딩한 문자열이 동일하지 않는 오류가 발생하여 해결한 파일
  * 읽어들인 파일명이 "ㅍㅏㅇㅣㄹ"과 같이 자모가 분리되어 유니코드로 입력 받기 때문에 인코딩해주어야 함
  * 최초에는 함수로 구현했으나 간단하게 해결 가능하여 해당 파일 내 main 함수를 참고하면 별도의 절차 없이 한글 인코딩이 가능함
  
* alertController.py
  * selenium 작동 중 팝업 알림창으로 인한 오류를 잡아주는 파일

* autoLogin.py
 * selenium을 이용한 chromedriver로 회계시스템에 로그인을 수행
 * 사용되는 로그인 아이디와 패스워드는 loginData.xlsx에서 작성
 * 부가적으로 필요한 함수 포함
 
* dateController.py
 

* errorController.py
* example.xlsx
* help.py
* help.txt
* ignoreAutoLogout.py
* main.py
* manage.py
* xlsxFileController.py
