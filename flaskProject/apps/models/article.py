from apps.models import db, func
from apps.models.board import Board
from apps.utils.utils import *


class BoardArticle(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, content, board_id, user_id):
        self.title = title
        self.content = content
        self.board_id = board_id
        self.user_id = user_id

    def __repr__(self):
        return '<id {}, board {}>'.format(self.id, self.board_id)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'time_created': self.time_created,
            'time_updated': self.time_updated,
            'board_id': self.board_id,
            'user_id': self.user_id
        }

    @staticmethod
    def read_article_list(limit, offset, board_id):
        """
        :param board_id
        :return: json(message,id,name)
        """
        try:
            article_list = BoardArticle.query \
                .filter_by(board_id=board_id) \
                .order_by(BoardArticle.time_updated.desc()) \
                .with_entities(BoardArticle.title) \
                .paginate(page=offset, per_page=limit)
            # article_list = BoardArticle.query.filter_by(board_id=board_id).with_entities(BoardArticle.title).all()
            return make_response(
                jsonify({
                    "message": "Get api",
                    str(BoardArticle.title).lower(): [i[0] for i in article_list]
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
    def create_article(title, content, board_id, cur_user):
        """
        :return json(message,id,name)
        """
        try:
            board = Board.query \
                .filter_by(id=board_id) \
                .first()
            new_article = BoardArticle(
                title=title,
                content=content,
                board_id=board.id,
                user_id=cur_user
            )
            db.session.add(new_article)
            db.session.commit()
            return make_response(
                jsonify({
                    "message": "Create api",
                    "id": new_article.id,
                    "board.id": new_article.board_id,
                    "title": new_article.title,
                    "content": new_article.content
                }), 200
            )
        except Exception as e:
            return make_response(
                jsonify({
                    "message": str(e)
                }), 500)

    @staticmethod
    def read_article(limit, offset, board_id, article_id):
        """
        :param board_id
        :param article_id
        :return: json
        """
        try:
            content = BoardArticle.query \
                .filter_by(board_id=board_id, id=article_id) \
                .order_by(BoardArticle.time_updated.desc()) \
                .with_entities(BoardArticle.content) \
                .paginate(page=offset, per_page=limit)
            return make_response(
                jsonify({
                    "message": "Get api",
                    str(BoardArticle.title): [i[0] for i in content]
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
    def update_article(new_title, new_content, cur_user, board_id, article_id):
        """
        :param board_id
        :param article_id
        :return json
        """
        try:
            new_article = BoardArticle.query \
                .filter_by(board_id=board_id, id=article_id, user_id=cur_user) \
                .first()
            if not new_article:
                return make_response(
                    jsonify({
                        "message": "Update api",
                        "state": False
                    }), 200
                )
            new_article.title = new_title
            new_article.content = new_content
            db.session.flush()
            db.session.commit()
            return make_response(
                jsonify({
                    "message": "Update api",
                    "id": new_article.id,
                    "new_title": new_article.title,
                    "new_content": new_article.content
                }), 200
            )
        except Exception as e:
            return make_response(
                jsonify({
                    "message": str(e)
                }), 500)

    @staticmethod
    def delete_article(cur_user, board_id, article_id):
        """
        :param board_id
        :param article_id
        :return json
        """
        try:
            del_article = BoardArticle.query \
                .filter_by(board_id=board_id, id=article_id, user_id=cur_user) \
                .delete()
            db.session.commit()
            return make_response(
                jsonify({
                    "message": "Delete api",
                    "state": True if del_article == 1 else False
                }), 200
            )
        except Exception as e:
            return make_response(
                jsonify({
                    "message": str(e)
                }), 500)

    @staticmethod
    def read_dashboard(n, limit, offset):
        """
        :return: json(message,id,name)
        """
        try:
            all_board = Board.query \
                .with_entities(Board.id)
            all_board = [i[0] for i in all_board]

            res = defaultdict(list)
            all_article = []
            for i in sorted(all_board):
                # res[i] = [i[0] for i in BoardArticle.query \
                #     .filter_by(board_id=i) \
                #     .order_by(BoardArticle.time_updated.desc()) \
                #     .limit(limit)\
                #     .with_entities(BoardArticle.title) \
                #     .paginate(page=offset, per_page=limit)]
                all_article.extend([i[0] for i in BoardArticle.query
                                   .filter_by(board_id=i)
                                   .order_by(BoardArticle.time_updated.desc())
                                   .limit(n)
                                   .with_entities(BoardArticle.title)])
            if offset != 1:
                idx = offset * limit
                return make_response(
                    jsonify({"articles": all_article[idx:idx + limit]}), 200
                )
            else:
                return make_response(
                    jsonify({"articles": all_article[:limit]}), 200
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
