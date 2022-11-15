# Mongo Dump
2022년 현대차증권에 On-premises로 설치된 Userhabit 프로젝트 내부 Mongo를 Dump하기 위해 제공하였다. \
해당 프로젝트의 Mongo 데이터 모델은 Userhabit Event, Session입니다.

## Dependency & Install
### Step by Step
1. Package List up: pip freeze > requirements.txt
2. Package Download: mkdir wheelhouse && pip download -r requirements.txt -d wheelhouse
3. Move: requirements.txt & mongoDump.py go to wheelhouse directory
4. Tar: tar -zcf wheelhouse.tar.gz wheelhouse
5. SCP: 파일 이동
6. 해당 서버에서 압축을 푼다. tar -zcf wheelhouse.tar.gz wheelhouse
7. 설치: pip install -r wheelhouse/requirements.txt --no-index --find-links wheelhouse --user

### Option
-r: requirements.txt 파일을 읽어 해당 모듈을 설치
--no-index --find-links: Offline으로 다운받은 모듈을 설치
--user: Local 현재 환경으로 설치

## Execution
mongoDump.py를 python3으로 실행시킵니다.
추가 파라미터로 true를 입력 받게 되면 뒤에 덤프할 To, From 날짜를 2022-01-01T00:00:00 형태로 추가로 입력합니다. 
```shell
python3 mongoDump.py {BOOL} {TO DATE} {FROM DATE}
```

## Model
TDO

## Code
1. Address, Path 및 Split Num 등 값을 conf.ini 파일에서 가져옵니다.
2. Session과 Event Collection에서 필드를 추출하여 Merge합니다.
3. 최종 결과는 data/ 디렉토리에 Dump된 .log파일과 log/ 디렉토리에 Dump 진행 log가 작성됩니다. 

## Log
```log
INFO:2022-06-30 18:06:42,665:BACKUP, From: 2021-01-11T00:00:00 To: 2022-06-11T23:59:59
DEBUG:2022-06-30 18:06:43,405:Created Mongo_Object_List_2022-06-30T18:06:42.log dump file.
DEBUG:2022-06-30 18:06:43,424:Created Mongo_View_List_2022-06-30T18:06:43.log dump file.
DEBUG:2022-06-30 18:06:46,476:Running...[ 5000 docs ] 0:00:02.943292
DEBUG:2022-06-30 18:06:49,349:Running...[ 10000 docs ] 0:00:05.816136
DEBUG:2022-06-30 18:06:50,562:Running...[ 15000 docs ] 0:00:07.029916
DEBUG:2022-06-30 18:06:53,393:Running...[ 20000 docs ] 0:00:09.860955
DEBUG:2022-06-30 18:06:56,217:Running...[ 25000 docs ] 0:00:12.684541
DEBUG:2022-06-30 18:06:57,468:Running...[ 30000 docs ] 0:00:13.935115
DEBUG:2022-06-30 18:07:00,306:Running...[ 35000 docs ] 0:00:16.773618
DEBUG:2022-06-30 18:07:01,525:Running...[ 40000 docs ] 0:00:17.992212
DEBUG:2022-06-30 18:07:04,374:Running...[ 45000 docs ] 0:00:20.841158
DEBUG:2022-06-30 18:07:07,263:Running...[ 50000 docs ] 0:00:23.730583
DEBUG:2022-06-30 18:07:08,474:Running...[ 55000 docs ] 0:00:24.941183
DEBUG:2022-06-30 18:07:11,313:Running...[ 60000 docs ] 0:00:27.780889
DEBUG:2022-06-30 18:07:14,222:Running...[ 65000 docs ] 0:00:30.689103
DEBUG:2022-06-30 18:07:15,420:Running...[ 70000 docs ] 0:00:31.887507
DEBUG:2022-06-30 18:07:18,240:Running...[ 75000 docs ] 0:00:34.707562
DEBUG:2022-06-30 18:07:19,432:Running...[ 80000 docs ] 0:00:35.899817
DEBUG:2022-06-30 18:07:22,280:Running...[ 85000 docs ] 0:00:38.747372
DEBUG:2022-06-30 18:07:25,120:Running...[ 90000 docs ] 0:00:41.587867
DEBUG:2022-06-30 18:07:26,541:Running...[ 95000 docs ] 0:00:43.008971
DEBUG:2022-06-30 18:07:28,427:Running...[ 100000 docs ] 0:00:44.894565
DEBUG:2022-06-30 18:07:28,433:Created Mongo_Raw_Data_2022-06-30T18:06:43.log dump file.
INFO:2022-06-30 18:07:28,435:Success. 0:00:45.770264 taken for make_session_event_backup method.
```

## Dump File
Object List와 View Lis 두 가지로 파일이 생성도됩니다.

### Object List
```log
Activity7.anotherListView081|Activity7.버튼1|별명1|
Activity7.anotherListView081|Activity7.버튼2|별명2|
Activity7.anotherListView291|Activity7.버튼3|별명3|
Activity7.anotherListView291|Activity7.버튼4| Object alias~~|
Activity7.anotherListView664|Activity7.Scene791ButtonB||
Activity7.anotherListView640|Activity7.Scene381ButtonB||
|Activity7.Scene896ButtonB||
|Activity7.Scene950ButtonB||
|Activity7.Scene394ButtonB||
```

### View List
```log
###SESSION_START###|세션별명1
(IntroActivity)|인트로 액티비티
Activity7.anotherListView081|액티비티7 리스트뷰81
Activity7.anotherListView291| view alias~~
Activity7.anotherListView640|액티비티 640뷰
Activity7.anotherListView664|액티비티7 리스트뷰664
###SESSION_END###|Alias test~~
Activity7.anotherListView091|
Activity7.anotherListView793|
```
