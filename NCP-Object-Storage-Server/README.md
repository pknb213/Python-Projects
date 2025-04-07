# 25.04.07
- Legacy 만드는 버튼을 두면 어떨까?!
- Upload Path 변경 어떻게 하면 될까?! DB 이용? 흠







## Todo List (10/15)
1. Project 테이블에서 Legacy 컬럼을 True로 할 부분을 찾지 못해서 추가 못함. (예상, 레거시 버튼 클릭 시, 일괄 True가 최선 일까?)

## Todo List (10/11)
1. learnetic_service.py 347줄에 있는 find_root_project_id를 결과 값을 루트 project_id 뿐만 아니라
    상위 프로젝트들의 id들을 리스트로 읽어와서 depth_1.... 처럼 넣고 저장하는 건 어떤가?
2. ✅ 330 print문 지우기 
3. ✅ conent_count도 누적해서 전달하면 어떨까? 얘는 어떻게 저장하고 project에 update하면 좋을지 모르겠네
4. log를 보니깐 3-1문서 넣을 때, Insert Error: 'file' is an invalid keyword argument for Lesson 발생함

## Todo List
1. ✅ Streamlit Project list를 DB를 보여주고, Request를 버튼 누르면 가져오는 걸로 변경
2. ✅ 현재 Project의 Status는 변경하도록 했음. 이걸 출력해야 함.

## Todo 24-06-21
1. ✅ Upload되는 파일명이 ENGL과 같이 특정 prefix과 다르면 업로드하지 않는다.
2. ✅ Export할 때 러너틱 권한 에러가 출력되면, 알 수 있어야 한다.
3. 서버 용량 확보 필요. 1) 다 올리고 삭제? 2) 올리고 바로 삭제? 3) 병렬로 동작 중이면 어느 시점에?
4. ✅ Streamlit 페이지에서 프로젝트 버튼을 누르면 Lesson Table을 가져오는 것으로 변경하자.

# 무결성 테스트
- DB: 645개 (project_id = 5602887601094656, export 2개 안함)
- ObjectStorage Files: 2 + 4 + 1 + 8 + 2 + 2 + 1 + 1 + 543 + 1 + 1 + 1 + 1 = 568개
- Project API Content Counter: 1025
- Logging 확인하니깐 몇 콜백에서 500에러가 존재함.
- lessons remain 603 + 50 = 653개
- 홈페이지 English | Splitted -> Middle School English 1 (Yoon) -> Lessons 653개

Export_lesson Error: {'status_code': 500, 'error': 'unexpected character: line 2 column 1 (char 1)'}

### 파일명에 / 슬래시 쳐 붙은 것도 있네
File Write Error: [Errno 2] No such file or directory: '/home1/ncloud/python/contents/English_Middle/High_Template.zip'
ERROR:root:[Errno 2] No such file or directory: '/home1/ncloud/python/contents/English_Middle/High_Template.zip

### ?
Module Path: /home1/ncloud/python/app
Token Error: {'status_code': 500, 'error': 'Cannot connect to host www.mauthor.com:443 ssl:default [None]'}
ERROR:root:{'status_code': 500, 'error': 'Cannot connect to host www.mauthor.com:443 ssl:default [None]'}
