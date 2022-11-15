# Context-Awareness-System 
해당 프로젝트는 2020년 유비벨록스 모바일에서 진행한 과제로 중소·중견 가전사의 IoT가전 제품개발 전주기 지원을 위한 빅데이터 상용화 플랫폼 기술 개발(20000195) 정부과제의 3차년도 개발 항목 상황인지 시스템 구현 프로젝트입니다.

## 목차
- [Introduce](#Introduce)
- [Development Environment](#Development-Environment)
- [Execution](#실행하기)

## Introduce
다음의 에브리봇 물걸레 청소기 기반 서비스 시나리오를 수행하는 Batch 서버입니다.
### case1
- 마지막 주기보고 시각을 기록합니다.
- 일정 시간이 경과 되고 나서 동작을 시작합니다.
- 내부 batch daemon이 분 단위로 체크를 합니다.
- 3분 경과시 와이파이 연결 상태 체크 관련 문구 notification 발생.

### case2
- RSSI 값을 매회 체크하여 일정 수치 이하로 감소시 동작합니다.
- 일시적인 하락으로 인한 오탐 방지 로직 검토 진행.

### Sequence Diagram
동작의 전반적인 구조는 아래 시퀸스 다이어그램과 같습니다.
<img src="https://user-images.githubusercontent.com/36396206/201862147-1fb83073-215c-4062-a522-9a136e68e8b3.png" width="50%" height="50%"/>

## Development Environment
- 기본 환경
  - IDE: Pycharm
  - OS: Linux CentOs
- Back-end
  - Python 3.8
  - Flask
  - APScheduler
  - Celery
  - Flask-restplus
  - Werkzeug
- PDF Reader Library
  - Pdfjs
- Front-end (HTML Page)
  - Jinja2
  - Javascript
- Database
  - MariaDB
  - Redis

### Setting environment variables
대부분 설정 변수가 하드코딩이 된 상태에서 Refactoring을 진행하지 않아, 제대로 된 동작하기 어렵다. \
또한 전체 동작을 현 코드 내에서 할 수 없는데는 아래 이유가 있다.
기본적으로 가전에서 송신되는 Socket을 받을 수 없고, 중간 API gateway으로 request를 전송하여 response를 수신 받아 \
해당 PDF 로직을 수행 후, Application으로 Noti를 전달하기 때문에 일련의 동작 시퀸스가 이루어 지기 어렵다.

### Execution
Flask 서버의 Url은 Swagger와 동일 합니다. \
기본 주소는 다음과 같으며 접속 시 아래 이미지와 같이 Swagger 문서를 확인할 수 있습니다. \
Base Url: `http://localhost:50000/`

<img src="https://user-images.githubusercontent.com/36396206/201884462-f9a830da-156d-40be-b056-5fc25faf90ce.png" width="50%" height="50%" />

