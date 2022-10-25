# Flask Board Example

This is an example of adding and deleting bulletin boards using Flask.

## Library

The libraries and versions used in the project are as follows.

### Database
- psycopg2-binary == 2.9.4
### DB Migration
- alembic == 1.8
### DB ORM
- Flask-SQLAlchemy == 3.0.1
- SQLAlchemy==1.4.41
### Server framework
- Flask == 2.2.2
- Werkzeug == 2.2.2
### Server function
- Flask-Login == 0.6.2
- Flask-Migrate == 3.1.0
### Session
- Flask-JWT-Extended == 4.4.4
- PyJWT == 2.5.0
- redis == 4.3.4

## Install
The installation sequence is as follows.
1. Install the module
2. Setting Environment Variables
3. Database initialization
### Module installation
Module installation uses the ***requirements.txt*** file.
```sh
$ pip install -r requirements.txt 
```

### Setting environment variables
The environment variables declared in the ***env.env*** file are applied through the terminal.
```sh
$ set -o allexport
$ source env.env
$ set +o allexport
```

### Database Initialize
Initialize the Postgresql database.
```sh
$ flask db init 
```

## API List
The API is as follows and the base url is localhost:5000.
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
For example, the sequence to delete a board after adding and updating a board and posting is as follows.

1. Call a SingUp API
```http request
POST http://localhost:5000/signup
Content-Type: application/x-www-form-urlencoded

fullname={FullName}&email={E-mail}&password={Password}
```
2. Call a Login API
```http request
POST http://localhost:5000/login
Content-Type: application/x-www-form-urlencoded

email={E-mail}&password={Password}
```
3.  Call a Board Create API
```http request
POST http://localhost:5000/board
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {Token}

board_name={Board Name}
```
4. Call a Article Create API
```http request
POST http://localhost:5000/article
Content-Type: application/x-www-form-urlencoded

title={Title}&content={Content}&board_id={Board Id}
```
5. Call a Article Update API
```http request
POST http://localhost:5000/article/{Board Id}/{Article Id}/update
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {Token}

new_title={New Title}&new_content={New Content}
```
6. Call a Article Delete API
```http request
POST http://localhost:5000/article/{Board Id}/{Article Id}/delete
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer {Token}
```

## Pagination

The pagination function is provided as limit and offset URL parameters only for the following APIs that get a list.

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

Database migration It is performed through the following CLI and a file is created in the migration directory.
```shell
$ flask db migrate -m "updated migration."
$ flask db upgrade
```

## Redis

In Redis, when a user logs in, it is stored and referenced in the form of a Hashmap as shown below.
```python
{
    Email: {
        logined: 1 or 0,
        last_login: datetime.now()
    }
        
}
```
