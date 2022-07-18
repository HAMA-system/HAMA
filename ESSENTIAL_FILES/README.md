##  **main.py**
* chromedriver를 사용하여 회계 시스템에 접속하고 다른 함수를 실행하도록 연결해주는 main 파일
* Lookup, Wirte 등 프로그램을 테스트할 때 해당 파일을 선택하여 테스트할 수 있음
 
##  **manage.py**
* 거의 대부분의 데이터를 처리하는 가장 핵심적인 파일
* Lookup, Write를 포함하여 그 과정에서 사용되는 Upload, Save 등 다양한 함수를 포함하고 있음

---

## **manage.py 내부 함수**

### lookup()
* 결의서를 조회하는 함수
* search() 함수를 호출하여 사용자가 선택한 조건에 따라 결의서를 조회함

### write()
* 결의서 자동 작성을 위한 함수
* HIDDEN_FILES/data.xlsx 엑셀 파일을 열어 15행부터 차례대로 입력을 수행함
* 입력이 없거나(_) 기존에 입력되어 블라인드 처리(-1)를 한 경우에는 수행을 중단함
* 현재는 입력이 단 한줄도 없으면 오류가 발생하면서 초기화면으로 돌아가도록 되어 있음
* 결의서 하나를 작성한 후에 사용자에게 확인을 받고 저장을 하게하면 write_ask 버전, 자동으로 저장하게 하면 write 버전임
* 자동 저장 여부는 save() 함수를 수정한 후 배포하면 됨
* 기존에는 저장 이후에 작성된 결의서는 엑셀의 구분번호를 '-1'로 바로 수정하도록 구현했으나 요청에 따라 수정하지 않도록 바꿨음

### taxWrite()
* 엑셀 파일 우측에 존재하는 세금 파트를 입력하는 함수

### taxWrite()
### taxWrite()
### modify()
### upload()
### save()
### delete()
### refresh()
### monthly_next()
### new_monthly_next()
### monthly_check()
### monthly_textReplace()
### month_inc
### ymonth_inc
### dorm()
### search()
* 결의서 조회를 위한 함수
* 조회 조건을 입력 받아 path값을 찾아서 결의서 조회

### modify_input()

