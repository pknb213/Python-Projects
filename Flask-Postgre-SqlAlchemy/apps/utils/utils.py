import string
from datetime import datetime
from flask import Flask, session, request, jsonify, make_response
from flask_migrate import Migrate
from flask_login import current_user, login_required
from werkzeug.exceptions import NotFound
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash
from redis import Redis, RedisError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

REDIS_URL = 'localhost'
# cache = Redis(host=REDIS_URL, port=25100, db=0)

# Clear Redis
# cache.flushdb()

KSQL_URL = "http://localhost:8088/ksql"
KSQL_QUERY_URL = "http://localhost:8088/query"
KSQL_HEADER = {
    "Accept": "application/vnd.ksql.v1+json",
    "Content-Type": "application/vnd.ksql.v1+json"
}


def ksql_response(msg: string, status_code: int, data: any = ""):
    """
    :returns @type, error_code, message, statementText, entities
    """
    return jsonify({
        "message": msg,
        "status_code": status_code,
        "data": {"query": data},
        "success": True if status_code == 200 else False
    })


def ok_response(msg: string, status_code: int = 200, data: any = ""):
    return jsonify({
        "message": msg,
        "status_code": status_code,
        "data": data,
        "success": True
    })


def error_response(msg: string, status_code: int = 404):
    return jsonify({
        "message": msg,
        "status_code": status_code,
        "data": "",
        "success": False
    })
