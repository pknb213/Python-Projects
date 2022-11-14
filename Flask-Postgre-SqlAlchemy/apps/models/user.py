import jwt
from apps.models import db, func
from apps.utils.utils import *


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    boards = db.relationship('Board', backref='users', lazy=True)
    articles = db.relationship('BoardArticle', backref='users', lazy=True)

    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'password': self.password,
            'time_created': self.time_created,
            'time_updated': self.time_updated,
        }

    @staticmethod
    def signup_post(name, email, password):
        user = User.query.filter_by(email=email).first()

        if user:
            return make_response(jsonify({
                "message": "Already exist user",
            }), 200)

        new_user = User(email=email, fullname=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify({
            "message": "Create user",
            "id": new_user.id,
            "email": new_user.email,
            "fullname": new_user.fullname
        }), 200)

    @staticmethod
    def login_post(email, password):
        user = User.query.filter_by(email=email).first()
        if user or check_password_hash(user.password, password):
            flag = 0 if cache.hget(email, "logined") is None else int(cache.hget(email, "logined"))
            if flag:
                return make_response(jsonify({
                    "message": "Already login user"
                }), 200)
            else:
                access_token = create_access_token(identity=user.id,
                                                   expires_delta=False)
                date = str(datetime.now())
                cache.hset(email, "logined", 1)
                cache.hset(email, "last_login", date)
                user.time_updated = datetime.now()
                db.session.commit()
            return make_response(jsonify({
                "message": "Login success",
                "id": user.id,
                "email": user.email,
                "fullname": user.fullname,
                "date": date,
                "token": access_token
            }), 200)

        else:
            return make_response(jsonify({
                "message": "Login fail",
            }), 200)

    @staticmethod
    def logout(email):
        flag = 0 if cache.hget(email, "logined") is None else int(cache.hget(email, "logined"))
        if flag:
            date = str(datetime.now())
            cache.hset(email, "logined", 0)
            cache.hset(email, "last_login", date)
            return make_response(jsonify({
                "message": "Logout success",
                "email": email,
                "date": date
            }), 200)
        else:
            return make_response(jsonify({
                "message": "Logout fail",
                "email": email
            }), 200)
