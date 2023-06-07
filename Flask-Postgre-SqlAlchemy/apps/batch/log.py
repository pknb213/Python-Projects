import json
import string, requests
from flask import make_response, jsonify, Request, Response, request

from apps import KSQL_URL, KSQL_HEADER, ok_response, error_response, ksql_response, KSQL_QUERY_URL, LOCAL_LOG_PATH
from apps.batch.dummy import job


class Log:
    def __init__(self, req):
        self.method = req.method

    @staticmethod
    def _to_json_from_ksql(_dict: dict):
        """
        header + columns => json
        """
        if len(_dict) < 1: return False
        try:
            schema = _dict[0]["header"]["schema"].replace(" ", "").replace("`", " ").lstrip().split(" ")[0::2]
            msg = _dict[-1]["finalMessage"] if "finalMessage" in _dict[-1] else "Success"
            if msg == "Success":
                result = [{schema[i]: row['row']['columns'][i] for i in range(len(schema))} for row in _dict[1:]]
            else:
                result = [{schema[i]: row['row']['columns'][i] for i in range(len(schema))} for row in _dict[1:-1]]
            return {
                "message": msg,
                "data": result
            }
        except Exception as e:
            print("Error: ", e)
            raise e

    @staticmethod
    def _convert_schema(schema: dict):
        try:
            result = ', '.join(f"`{key}` {value}" for key, value in schema.items())
            return result
        except Exception as e:
            print("Error: ", e)
            raise e

    @staticmethod
    def received_log(log: string) -> Response:
        try:
            path = LOCAL_LOG_PATH
            job(path, log)
            return ok_response(
                "Success, Written Log",
                data=log
            )
        except Exception as e:
            return error_response(e)

    @staticmethod
    def show_topics():
        try:
            url = KSQL_URL
            headers = KSQL_HEADER
            data = {
                "ksql": f"""
                    show topics;
                """,
                "streamsProperties": {
                    "ksql.streams.auto.offset.reset": "earliest"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            if response.status_code == 200:
                return ksql_response(
                    msg=response.json()[0]["topics"],
                    status_code=response.status_code,
                    data=response.json()[0]["statementText"],
                )
            else:
                return ksql_response(
                    msg=response.json()['message'],
                    status_code=response.status_code,
                    data=response.json()["statementText"]
                )
        except Exception as e:
            return error_response(e)

    @staticmethod
    def show_streams():
        try:
            url = KSQL_URL
            headers = KSQL_HEADER
            data = {
                "ksql": f"""
                    show streams;
                """,
                "streamsProperties": {
                    "ksql.streams.auto.offset.reset": "earliest"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            if response.status_code == 200:
                return ksql_response(
                    msg=response.json()[0]["streams"],
                    status_code=response.status_code,
                    data=response.json()[0]["statementText"],
                )
            else:
                return ksql_response(
                    msg=response.json()['message'],
                    status_code=response.status_code,
                    data=response.json()["statementText"]
                )
        except Exception as e:
            return error_response(e)

    @staticmethod
    def show_tables():
        try:
            url = KSQL_URL
            headers = KSQL_HEADER
            data = {
                "ksql": f"""
                    show tables;
                """,
                "streamsProperties": {
                    "ksql.streams.auto.offset.reset": "earliest"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            if response.status_code == 200:
                return ksql_response(
                    msg=response.json()[0]["tables"],
                    status_code=response.status_code,
                    data=response.json()[0]["statementText"],
                )
            else:
                return ksql_response(
                    msg=response.json()['message'],
                    status_code=response.status_code,
                    data=response.json()["statementText"]
                )
        except Exception as e:
            return error_response(e)

    @staticmethod
    def create_stream(topic: string, stream_name: string, schema: dict):
        try:
            url = KSQL_URL
            headers = KSQL_HEADER
            data = {
                "ksql": f"""
                    create stream {stream_name} (
                        {Log._convert_schema(schema)}
                    ) with (
                        KAFKA_TOPIC = '{topic}',
                        VALUE_FORMAT = 'JSON'
                    );
                """,
                "streamsProperties": {
                    "ksql.streams.auto.offset.reset": "earliest"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            if response.status_code == 200:
                return ksql_response(
                    msg=response.json()[0]["commandStatus"]["message"],
                    status_code=response.status_code,
                    data=response.json()[0]["statementText"],
                )
            else:
                return ksql_response(
                    msg=response.json()['message'],
                    status_code=response.status_code,
                    data=response.json()["statementText"]
                )
        except Exception as e:
            return error_response(e)

    @staticmethod
    def get_stream(stream_name):
        try:
            url = KSQL_QUERY_URL
            headers = KSQL_HEADER
            data = {
                "ksql": f"""
                    select * from {stream_name};
                """,
                "streamsProperties": {
                    "ksql.streams.auto.offset.reset": "earliest"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            if response.status_code == 200:
                res = Log._to_json_from_ksql(response.json())
                return ksql_response(
                    msg=res["message"],
                    status_code=response.status_code,
                    data=res["data"]
                )
            else:
                return ksql_response(
                    msg=response.json()['message'],
                    status_code=response.status_code,
                    data=response.json()["statementText"]
                )
        except Exception as e:
            return error_response(e)

    @staticmethod
    def create_table(table_name: string, select_query: string):
        try:
            url = KSQL_URL
            headers = KSQL_HEADER
            data = {
                "ksql": f"""
                    create table {table_name} as {select_query}
                        EMIT CHANGES;
                    """,
                "streamsProperties": {
                    "ksql.streams.auto.offset.reset": "earliest"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            if response.status_code == 200:
                return ksql_response(
                    msg=response.json()[0]["commandStatus"]["message"],
                    status_code=response.status_code,
                    data=response.json()[0]["statementText"],
                )
            else:
                return ksql_response(
                    msg=response.json()['message'],
                    status_code=response.status_code,
                    data=response.json()["statementText"]
                )
        except Exception as e:
            return error_response(e)

    @staticmethod
    def get_table(table_name: string):
        try:
            url = KSQL_QUERY_URL
            headers = KSQL_HEADER
            data = {
                "ksql": f"""
                        select * from {table_name};
                    """,
                "streamsProperties": {
                    "ksql.streams.auto.offset.reset": "earliest"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            if response.status_code == 200:
                res = Log._to_json_from_ksql(response.json())
                return ksql_response(
                    msg=res["message"],
                    status_code=response.status_code,
                    data=res["data"]
                )
            else:
                return ksql_response(
                    msg=response.json()['message'],
                    status_code=response.status_code,
                    data=response.json()["statementText"]
                )
        except Exception as e:
            return error_response(e)

    @staticmethod
    def select_query(query: string):
        try:
            url = KSQL_URL
            headers = KSQL_HEADER
            data = {
                "ksql": f"""{query};""",
                "streamsProperties": {
                    "ksql.streams.auto.offset.reset": "earliest"
                }
            }

            response = requests.post(url, headers=headers, json=data)
            print(response.json())
            if response.status_code == 200:
                return ksql_response(
                    msg=response.json()[0]["commandStatus"]["message"],
                    status_code=response.status_code,
                    data=response.json()[0]["statementText"],
                )
            else:
                return ksql_response(
                    msg=response.json()['message'],
                    status_code=response.status_code,
                    data=response.json()["statementText"]
                )
        except Exception as e:
            return error_response(e)
