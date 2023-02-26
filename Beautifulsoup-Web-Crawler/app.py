from flask import Flask, render_template, make_response, jsonify, request

from src.RemoteOk import RemoteOk
from src.WeworkRemotely import WeworkRemotely

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def show_results():
    search_string = request.form.get('search_string')
    remote_ok_res = RemoteOk(search_string).extract()
    wework_remotely_res = WeworkRemotely(search_string).extract()

    res = remote_ok_res + wework_remotely_res
    print(res)
    return make_response(jsonify(res), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
