import string, requests
from flask import make_response, jsonify, Request, Response, request

from apps.batch.dummy import job


class Log:
    def __init__(self, req):
        self.method = req.method

    @staticmethod
    def received_log(args: string, body: Request.json) -> Response:
        try:
            print("Json:\n", body, "\nArgs:\n", args["is_file"])
            if "log" not in body: raise "Invalid Log !!"
            log = body["log"]
            if args["is_file"].strip().lower() == 'y':
                path = "/Users/yj/fluent-bit/data/input/test.txt"
                job(path, log)
            else:
                url = "http://localhost:8088/ksql"
                headers = {
                    "Accept": "application/vnd.ksql.v1+json",
                    "Content-Type": "application/vnd.ksql.v1+json"
                }

                data = {
                    # "ksql": "CREATE STREAM status_cnt AS SELECT * FROM pageviews_original WHERE pageid='home'; CREATE STREAM pageviews_alice AS SELECT * FROM pageviews_original WHERE userid='alice';",
                    "ksql": """
                        create stream error_count as select
                            select * from test t 
                            where t.value['level'] = 'ERROR'
                    """,
                    "streamsProperties": {
                        "ksql.streams.auto.offset.reset": "earliest"
                    }
                }

                response = requests.post(url, headers=headers, json=data)
                print(response.status_code)
                print(response.json())

                pass
            return make_response(jsonify({
                "message": "Success",
                "data": log
            }), 200)
        except Exception as e:
            print("Fail:", e)
            return make_response(jsonify({
                "message": e,
                "data": None
            }), 404)
