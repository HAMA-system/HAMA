# HAMA
Hongik Accounting Management Advanced System

```
 __  __  ______  __    __  ______       ______  __  __  ______  ______  ______  __    __
/\ \_\ \/\  __ \/\ "-./  \/\  __ \     /\  ___\/\ \_\ \/\  ___\/\__  _\/\  ___\/\ "-./  \
\ \  __ \ \  __ \ \ \-./\ \ \  __ \    \ \___  \ \____ \ \___  \/_/\ \/\ \  __\\ \ \-./\ \
 \ \_\ \_\ \_\ \_\ \_\ \ \_\ \_\ \_\    \/\_____\/\_____\/\_____\ \ \_\ \ \_____\ \_\ \ \_\
  \/_/\/_/\/_/\/_/\/_/  \/_/\/_/\/_/     \/_____/\/_____/\/_____/  \/_/  \/_____/\/_/  \/_/
   
```

## Project Info

### Made by
[2022.3.17 ~ ]
* **Minseok-Kim**, Hongik-Univ. Computer Engineering Dept. - https://github.com/pxxnxx
* **Taehee-Han**, Hongik-Univ. Computer Engineering Dept. - https://github.com/110w110

### Maintained by
* (Not yet)

### VCS repo
* Github :: https://github.com/HAMA-system

## Files

### Essential Files
 
####  **main.py**
* chromedriver를 사용하여 회계 시스템에 접속하고 다른 함수를 실행하도록 연결해주는 main 파일
* Lookup, Wirte 등 프로그램을 테스트할 때 해당 파일을 선택하여 테스트할 수 있음
 
####  **manage.py**
* 거의 대부분의 데이터를 처리하는 가장 핵심적인 파일
* Lookup, Write를 포함하여 그 과정에서 사용되는 Upload, Save 등 다양한 함수를 포함하고 있음
* 파일 내부 함수에 대한 자세한 내용은 별첨

---
### Execute Files

#### **RUN_LOOKUP.py**
* 기간, 결의서 내용 등으로 편리하게 결의서 검색하기 위한 실행파일
  
#### **RUN_REPLACE.py**
* 결의서 첨부파일을 키워드에 맞게 폴더로 분류해주기 위한 실행파일
  
#### **RUN_WRITE.py**
* data.xlsx 파일을 읽어들여 자동으로 결의서를 작성하기 위한 실행파일
  
#### **RUN_DRAFT.py**
* 기안 작성을 위한 실행파일
  
####  ~~RUN_MODIFY.py~~
* 결의서 수정을 위한 실행파일
* RUN_DRAFT와 합쳐졌음 (07.13)
  
---
### Function Library
  
####  KorStringRecognizer.py
* 프로그램 내부에서 osdir을 통해 읽어들인 파일명과 하드코딩한 문자열이 동일하지 않는 오류가 발생하여 해결한 파일
* 읽어들인 파일명이 "ㅍㅏㅇㅣㄹ"과 같이 자모가 분리되어 유니코드로 입력 받기 때문에 인코딩해주어야 함
* 최초에는 함수로 구현했으나 간단하게 해결 가능하여 해당 파일 내 main 함수를 참고하면 별도의 절차 없이 한글 인코딩이 가능함
	 
####  dateController.py
* 날짜 형식을 원하는 형태로 수정하기 위한 파일
* 사용 예시는 파일 내 main 함수를 참조

####  errorController.py
* 프로그램 내에서 발생하는 다양한 오류 사항을 메시지로 정리해놓는 파일
* 현재는 xlsxFileController 등에서만 사용되고 많이 사용하지 않았음
	 
####  xlsxFileController.py
* 엑셀 파일을 읽어오고 자료구조에 정리하기 위한 파일
* 셀 하나의 입력, 한 행 입력, 한 열 입력 등 필요한 대부분의 기능이 구현되어 있음
	 
####  help.py
* 사용자에게 제공되는 도움말
* 구현은 완료되어 있으나 현재는 실행파일에 포함되지 않았음
 
####  help.txt
* help.py 파일에서 읽어들이는 텍스트 파일
* 긴 길이의 도움말을 텍스트 파일에서 작성하도록 하였음
* <a>와 </a>의 형태로 문자열을 구별하여 읽어들임

####  alertController.py
* selenium 작동 중 팝업 알림창으로 인한 오류를 잡아주는 파일

####  autoLogin.py
* selenium을 이용한 chromedriver로 회계시스템에 로그인을 수행
* 사용되는 로그인 아이디와 패스워드는 loginData.xlsx에서 작성
* 부가적으로 필요한 함수 포함

####  ignoreAutoLogout.py
* 회계 시스템에 로그인한 채 장시간 방치할 때 자동 로그아웃이 되지 않도록 방지하는 파일
	
---
### Temporary Files

#### _ttest_
* Replace 테스트를 위한 임시 폴더
  
####  .DS_Store
* Mac 환경에서 자동으로 생성되는 파일로 삭제해도 되는 파일  

---
### Hidden Files

#### data.xlsx
* 결의서 작성을 위해 미리 작성하도록 만들어진 엑셀 시트
* 거래처 또는 관리코드를 파일 내에서 검색할 수 있고, 정기적으로 입력되는 내용은 키워드로 등록해두면 키워드만 작성해도 전체가 작성되도록 편리하게 만들어짐
* 'data.xlsx' 파일 사용과 관련된 내용은 파일 내부 메모 기능을 통해 설명되어 있음
* 해당 파일의 대부분의 셀은 모두 수식으로 작성되어, 한 번 작성한 후 지우게 되면 기능을 잃으므로, 사용한 셀 또는 행을 지울 경우, 행 삭제를 통해 한 줄씩 모두 지우시는 것이 권장됨
* 기존에 준비된 서식은 약 500개 가량의 행이 준비되어 있으므로, 모든 행을 다 사용한 경우에는 백업파일을 복구하여 사용해야 함

#### linkData.py
* selenium에서 필요로 하는 다양한 xpath 값과 테스트하는 디바이스 별로 다른 절대경로를 따로 입력해두기 위한 파일

#### loginData.xlsx
* 회계 시스템에 접속하는 계정을 등록하는 파일

---
### Etc

####  _icon_
* Lookup, Modify, Write, Draft, Replace 등 실행파일에 사용될 아이콘 파일들
  
####  .gitignore
* 공개하지 않는 파일과 디바이스 별 다른 파일 등이 git에 올라가지 않도록 작성됨


 

  
