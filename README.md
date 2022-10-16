# mini_project

엘리스 미니 프로젝트 Backend Team Interview Project (2022)

## Library

사용한 라이브러리와 버전은 다음과 같습니다.
- alembic == 1.8
- Flask-SQLAlchemy == 3.0.1
- SQLAlchemy==1.4.41
- Flask == 2.2.2
- Flask-JWT-Extended == 4.4.4
- Flask-Login == 0.6.2
- Flask-Migrate == 3.1.0
- PyJWT == 2.5.0
- Werkzeug == 2.2.2
- psycopg2-binary == 2.9.4
- redis == 4.3.4

## Install

### 모듈 설치

```sh
$ pip install -r requirements.txt 
```

### 환경 변수 설정
env.env 파일에 선언한 환경 변수를 터미널을 통해 적용합니다.
```sh
$ set -o allexport
$ source env.env
$ set +o allexport
```

### DB Init
Database init을 합니다
```sh
$ flask db init 
```

## API List
API는 다음과 같으며 base url은 localhost:5000입니다.
1. User APIs
   - SignUp API : POST /signup
   - Login API : POST /login
   - Logout API : POST /logout
2. Board APIs 
   - Create API : POST /board
   - List API : GET /board_list
   - Update API : POST /board/<board_id>/update
   - Delete API : POST /board/<board_id>/delete
   - ArticleList API : GET /article_list/<board_id>
3. BoardArticle APIs
   - Create API : POST /article
   - Get API : GET /article/<board_id>/<article_id>
   - Update API : POST /article/<board_id>/<article_id>/update
   - Delete API : POST /article/<board_id>/<article_id>/delete
4. Dashboard APIs
   - RecentBoardArticle API : GET /dashboard

## Example
예시로 보드 추가 및 게시글 추가 및 업데이트 후, 삭제하는 시퀸스는 다음과 같습니다.

1. SingUp API를 호출
```http request
POST http://localhost:5000/signup
Content-Type: application/x-www-form-urlencoded

fullname={FullName}&email={E-mail}&password={Password}
```
2. Login API를 호출
```http request
POST http://localhost:5000/login
Content-Type: application/x-www-form-urlencoded

email={E-mail}&password={Password}
```
3.  Board Create API를 호출
```http request
POST http://localhost:5000/board
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {Token}

board_name={Board Name}
```
4. Article Create API를 호출
```http request
POST http://localhost:5000/article
Content-Type: application/x-www-form-urlencoded

title={Title}&content={Content}&board_id={Board Id}
```
5. Article Update API를 호출
```http request
POST http://localhost:5000/article/{Board Id}/{Article Id}/update
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {Token}

new_title={New Title}&new_content={New Content}
```
6. Article Delete API를 호출
```http request
POST http://localhost:5000/article/{Board Id}/{Article Id}/delete
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {Token}
```

## Pagination

Pagination 기능은 목록을 가져오는 다음의 API에 한하여 limit, offset URL Parameter로 제공합니다.

- /board_list
- /article_list/<board_id>
- /article/<board_id>/<article_id>
- /dashboard

```http request
POST http://localhost:5000article_list/{board_id}?limit={Limit}&offset={Offset}
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {Token}
```

## Postgresql Migration

Database migration 다음 cli를 통해 수행되며 migration 디렉토리에 파일이 생성됩니다.
```shell
$ flask db migrate -m "updated migration."
$ flask db upgrade
```

## Redis

Redis는 User가 Login 하게 되면 아래와 같이 Hashmap 형태로 저장하고 참고합니다.
```python
{
    Email: {
        logined: 1 or 0,
        last_login: datetime.now()
    }
        
}
```
