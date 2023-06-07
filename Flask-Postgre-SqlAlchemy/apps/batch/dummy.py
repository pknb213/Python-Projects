import datetime
import hashlib
import random
import string

import schedule
import time

from flask import make_response, jsonify

from apps import LOCAL_LOG_PATH


# from apps.kafka.inference_consumer import *


# def job(file):
#     print("working", datetime.datetime.now())
#     line = "[Info] [Date: {}] Writing...[Hash:{}]\n".format(datetime.datetime.now(), hashlib.md5("Hello".encode()).hexdigest())
#     file.write(line)
#     file.flush()

def generate_dummy_log():
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_code = ["ERROR", "WARN", "INFO", "DEBUG"]
    error = random.choice(error_code)
    status_code = [500, 404, 200]
    code = random.choice(status_code)
    msg = "Request processed successfully" if code == 200 else "Request processed fail"
    methods = ["GET", "POST", "DELETE", "PUT"]
    method = random.choice(methods)
    api_path = f"/api/users/{random.randint(0,1000)}"
    res = f"[{date}] [{error}] [HTTP] [{code}] {msg}: {method} {api_path}\n"
    return res


def job(file_path, logs: string = None):
    with open(file_path, 'a') as file:
        print("working", datetime.datetime.now())
        if not logs:
            # line = "[Info] [Date: {}] Writing...[Hash:{}]\n".format(datetime.datetime.now(), hashlib.md5("Hello".encode()).hexdigest())
            line = generate_dummy_log()
        else:
            line = logs + "\n"
        file.writelines(line)
        file.flush()


class Dummy:
    def __init__(self, seconds):
        self.seconds = seconds
        self.file_path = LOCAL_LOG_PATH

    def execute_job(self):
        print("Start Job")
        # file = open(self.file_path, 'w')
        schedule.every(1).seconds.do(job, file_path=self.file_path)
        while self.seconds:
            schedule.run_pending()
            time.sleep(1)
            self.seconds -= 1
            print("Remain Time: ", self.seconds)
        # file.close()
        return make_response(jsonify({
            "message": "Batch End",
        }), 200)
