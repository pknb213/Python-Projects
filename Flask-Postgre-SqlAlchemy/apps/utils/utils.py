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
