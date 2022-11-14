from apps.models import db, func
from apps.utils.utils import *


class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    articles = db.relationship('BoardArticle', backref='boards', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, user_id, articles=[]):
        self.name = name
        self.user_id = user_id
        self.articles = articles

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'time_created': self.time_created,
            'time_updated': self.time_updated,
            'articles': self.articles,
            'user_id': self.user_id
        }

    @staticmethod
    def create_board(cur_user, board_name):
        """
        :return json(message,id,name)
        """
        try:
            new_board = Board(name=board_name, user_id=cur_user)
            db.session.add(new_board)
            db.session.commit()
            return make_response(
                jsonify({
                    "message": "Added new board",
                    "id": new_board.id,
                    "name": new_board.name
                }), 200
            )
        except Exception as e:
            return make_response(
                jsonify({
                    "message": str(e)
                }), 500)

    @staticmethod
    def read_board_list(limit, offset):
        """
        :return: json(message,id,name)
        """
        try:
            board_list = Board.query \
                .with_entities(Board.name) \
                .paginate(page=offset, per_page=limit)
            return make_response(
                jsonify({
                    "message": "Get Board List",
                    str(Board.name).lower(): [i[0] for i in board_list]
                }), 200
            )
        except NotFound as e:
            return make_response(
                jsonify({
                    "message": e.description
                }), e.code)
        except Exception as e:
            return make_response(
                jsonify({
                    "message": str(e)
                }), 500)

    @staticmethod
    def update_board(cur_user, new_name, board_id):
        """
        :param board_id
        :return json(message,id,name)
        """
        try:
            board = Board.query \
                .filter_by(id=board_id, user_id=cur_user) \
                .first()
            if not board:
                return make_response(
                    jsonify({
                        "message": "Update api",
                        "state": False
                    }), 200
                )
            setattr(board, 'name', new_name)
            db.session.flush()
            db.session.commit()
            return make_response(
                jsonify({
                    "message": "Update api",
                    "id": board.id,
                    "name": board.name
                }), 200
            )
        except Exception as e:
            return make_response(
                jsonify({
                    "message": str(e)
                }), 500)

    @staticmethod
    def delete_board(cur_user, board_id):
        """
        :param board_id
        :return json(message,id,name)
        """
        try:
            board = Board.query \
                .filter_by(id=board_id, user_id=cur_user) \
                .delete()
            db.session.commit()
            return make_response(
                jsonify({
                    "message": "Delete api",
                    "state": True if board == 1 else False
                }), 200
            )
        except Exception as e:
            return make_response(
                jsonify({
                    "message": str(e)
                }), 500)
