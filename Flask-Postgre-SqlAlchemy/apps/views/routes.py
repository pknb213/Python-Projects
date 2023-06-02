from apps.batch.log import Log
from apps.utils.utils import *
from app import app
from apps.models.user import *
from apps.models.board import *
from apps.models.article import *
from apps.batch.dummy import *


@app.route('/')
def hello_world():
    return make_response(jsonify({"Message": "Hello World"}), 200)


@app.route('/batch/dummy', methods=['GET'])
def generated_dummy():
    dummy = Dummy(1800)
    return Dummy.execute_job(dummy)


@app.route('/log', methods=['POST'])
def post_log():
    body = request.json
    query = request.args
    return Log.received_log(query, body)


@app.route('/signup', methods=['POST'])
def sing_up():
    name = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    return User.signup_post(name, email, password)


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return User.login_post(email, password)


@app.route('/logout', methods=["POST"])
def logout():
    email = request.form.get('email')
    return User.logout(email)


@app.route("/board", methods=["POST"])
@jwt_required()
def post_create_board():
    cur_user = get_jwt_identity()
    board_name = request.form.get("board_name")
    return Board.create_board(cur_user, board_name)


@app.route("/board_list", methods=["GET"])
def get_board_list():
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 1, type=int)
    return Board.read_board_list(limit, offset)


@app.route("/board/<int:board_id>/update", methods=["POST"])
@jwt_required()
def post_update_board(board_id):
    cur_user = get_jwt_identity()
    new_name = request.form.get("new_name")
    return Board.update_board(cur_user, new_name, board_id)


@app.route("/board/<int:board_id>/delete", methods=["POST"])
@jwt_required()
def post_delete_board(board_id):
    cur_user = get_jwt_identity()
    return Board.delete_board(cur_user, board_id)


@app.route("/article_list/<int:board_id>", methods=["GET"])
def get_article_list(board_id):
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 1, type=int)
    return BoardArticle.read_article_list(limit, offset, board_id)


@app.route("/article", methods=["POST"])
@jwt_required()
def post_create_article():
    title = request.form.get("title")
    content = request.form.get("content")
    board_id = request.form.get("board_id")
    cur_user = get_jwt_identity()
    return BoardArticle.create_article(title, content, board_id, cur_user)


@app.route("/article/<int:board_id>/<int:article_id>", methods=["GET"])
def get_article(board_id, article_id):
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 1, type=int)
    return BoardArticle.read_article(limit, offset, board_id, article_id)


@app.route("/article/<int:board_id>/<int:article_id>/update", methods=["POST"])
@jwt_required()
def post_update_article(board_id, article_id):
    new_title = request.form.get("new_title")
    new_content = request.form.get("new_content")
    cur_user = get_jwt_identity()
    return BoardArticle(new_title, new_content, cur_user, board_id, article_id)


@app.route("/article/<int:board_id>/<int:article_id>/delete", methods=["POST"])
@jwt_required()
def delete_article(board_id, article_id):
    cur_user = get_jwt_identity()
    return BoardArticle.delete_article(cur_user, board_id, article_id)


@app.route("/dashboard", methods=["GET"])
def get_dashboard():
    n = request.args.get('n', 10, type=int)
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 1, type=int)
    return BoardArticle.read_dashboard(n, limit, offset)