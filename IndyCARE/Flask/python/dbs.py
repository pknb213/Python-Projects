# Todo : SQL_Alchemy로 변경해야 합니다.
import pymysql
from redis import Redis, RedisError

REDIS_URL = 'localhost'
cache = Redis(host=REDIS_URL, port=6379, db=0)

# Clear Redis
print("Remain Redis : ", cache.keys())
cache.flushdb()

INTERNAL_DATABASE = True  # Todo : True is AWS, False is Internal DB
DictCursor = pymysql.cursors.DictCursor


class MySQL:
    @staticmethod
    def connect():
        if INTERNAL_DATABASE:
            db = pymysql.connect(host='13.209.42.91',
                                 port=3306,
                                 user='inventory_admin',
                                 password='nrmk2013',
                                 db='indycare',
                                 charset='utf8')
        else:
            db = pymysql.connect(host='172.23.254.121',
                                 port=3306,
                                 user='root',
                                 password='nrmk2013',
                                 db='indycare',
                                 charset='utf8')
        return db

    @classmethod
    def select(cls, __str, multi=True):
        if type(__str) is str:
            try:
                db = MySQL.connect()
                with db.cursor(DictCursor) as cursor:
                    sql = __str
                    if cursor.execute(sql):
                        if multi:
                            res = cursor.fetchall()
                            return res
                        elif not multi:
                            res = cursor.fetchone()
                            return res
                    else:
                        return None
            except Exception as e:
                print("Select Error", e)
                raise e
            finally:
                cursor.close()
                db.close()
        else:
            raise Exception("Please, parameter must be String !")

    @classmethod
    def insert(cls, __str):
        if type(__str) is str:
            try:
                db = MySQL.connect()
                with db.cursor(DictCursor) as cursor:
                    sql = __str
                    cursor.execute(sql)
                db.commit()
                return False if cursor.lastrowid == 0 else True
            except Exception as e:
                print("Insert Error", e)
                raise e
            finally:
                cursor.close()
                db.close()
        else:
            raise Exception("Please, parameter must be String !")


