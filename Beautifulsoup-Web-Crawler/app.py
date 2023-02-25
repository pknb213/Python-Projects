from flask import Flask
from src.extract import extract_jobs
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    jobs = extract_jobs("golang")
    return jobs


if __name__ == '__main__':
    app.run()