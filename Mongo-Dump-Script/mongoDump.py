import os
import pymongo
import datetime
from bson.json_util import dumps
from functools import wraps
import sys
import logging
import configparser
import time

properties = configparser.ConfigParser()
properties.read("./conf.ini")
DUMP_PATH = properties["PATH"]["dump_path"]
LOG_PATH = properties["PATH"]["log_path"]

SPLIT_LINE_NUMBER = int(properties["DUMP"]["split_num"])

MONGO_ADDRESS = "mongodb://{user}:{pwd}@{addr}:{port}/?authSource={db}".format(
    user=properties["DB"]["User"],
    pwd=properties["DB"]["Pwd"],
    addr=properties["DB"]["Address"],
    port=int(properties["DB"]["Port"]),
    db=properties["DB"]["Mongodb"]
)

if not os.path.isdir(DUMP_PATH):
    os.mkdir(DUMP_PATH)
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)


class DumpException:
    """
    Not Used
    """
    def __init__(self):
        sections = [i for i in properties]
        keys = [key for section in properties for key in properties[section]]
        self.res = True
        for key in keys:
            if "DB" in sections or "PATH" in sections:
                if key == "user":
                    self.user = properties["DB"][key]
                elif key == "pwd":
                    self.pwd = properties["DB"][key]
                elif key == "mongodb":
                    self.mongodb = properties["DB"][key]
                elif key == "address":
                    self.address = properties["DB"][key]
                elif key == "port":
                    self.port = properties["DB"][key]
                elif key == "dump_path":
                    self.dump_path = properties["PATH"][key]
                elif key == "log_path":
                    self.log_path = properties["PATH"][key]
                elif key == "split_num":
                    self.split_num = properties["DUMP"][key]
                else:
                    logging.error("Please checked conf.ini file.")
                    self.res = False

    @staticmethod
    def exception_by_address(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # try:
            #     tmp = auth[1].split(":")
            #     host, port = tmp[0], tmp[1]
            #     ip_l = len(host.split("."))
            #     if host != "localhost" and ip_l != 4:
            #         logging.error("Invalid Host Address or Port.", exc_info=True)
            #         exit(1)
            # except Exception as e:
            #     logging.error("Invalid Parameter. please checked db url. ( mongodb://{ID}:{PW}@{HOST}:{PORT} )", exc_info=True)
            #     exit(1)
            pass
        return wrapper()

    @staticmethod
    def exception_by_argument(self):
        def wrapper(*args, **kwargs):
            pass
        return wrapper()

    @staticmethod
    def exception_by_mongo(self):
        def wrapper(*args, **kwargs):
            pass
        return wrapper()


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        logging.info(f'Success. {end-start} taken for {func.__name__} method.\n')
        return result
    return wrapper


def transforming(_str, coll_name):
    """
    :param _str: String
    :return: String
    """
    if coll_name == "Mongo_View_List_":
        return "{0}|{1}".format(_str["vi"], _str["alias"])
    if coll_name == "Mongo_Object_List_":
        return "{0}|{1}|{2}|".format(_str["vi"], _str["oi"], _str["alias"])


def create_dump_file(doc_list, name, right):
    """
    :param doc_list: Documents
    :param name: Filename
    :param right: open() method parameter
    :return: void
    """
    # file_date_string = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    cnt = 0
    # path = DUMP_PATH + "" + name + file_date_string + ".log"
    st = datetime.datetime.now()
    # len_doc = len(doc_list)
    # if not len_doc:
    #     logging.debug(name + "is empty")
    if not doc_list:
        logging.debug(name + "is empty")
    else:
        # while len_doc > cnt:
        file_date_string = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        path = DUMP_PATH + "" + name + file_date_string + ".log"
        with open(path, right, encoding="UTF-8") as f:
            # for i in doc_list[cnt:]:
            for i in doc_list:
                if name == "Mongo_View_List_" or name == "Mongo_Object_List_":
                    if "alias" not in i:
                        i["alias"] = ""
                    if "vi" not in i:
                        i["vi"] = ""
                    i = transforming(i, name)
                    try:
                        f.write(dumps(i, ensure_ascii=False).replace("\"", "")+"\n")
                    except Exception as e:
                        logging.debug("Object list dump failed : {0}".format(e))
                        raise e
                else:
                    try:
                        f.write(dumps(i, ensure_ascii=False)+"\n")
                    except Exception as e:
                        logging.debug("View list dump failed : {0}".format(e))
                        raise e
                # f.write("\n")
                f.flush()
                cnt += 1
                # logging.info(name + " - " + str(cnt))
                if cnt % SPLIT_LINE_NUMBER == 0:
                    logging.debug("Running...[ {doc} ] {time}".format(doc=str(cnt)+" docs", time=datetime.datetime.now()-st))
                    # f.close()
                    # time.sleep(1)
                    # break

        logging.debug("Created {} dump file.".format(name + file_date_string + ".log"))


def object_qry(coll):
    """
    :param coll: MongoDB Collection
    :return: List Type Documents
    """
    pipe = [
        {
            "$lookup": {
                "from": "view_list_pt24h",
                "localField": "vhi",
                "foreignField": "vhi",
                "as": "view"
            }
        },
        {"$replaceWith": {"$mergeObjects": [{
            "vi": {"$arrayElemAt": ["$view.vi", 0]},
            "oi": "$oi",
            "alias": "$alias"
        }]}}
    ]
    try:
        # res = list(coll.aggregate(pipe))
        res = coll.aggregate(pipe)
        # logging.debug("Object list document count : {0}".format(len(res)))
    except Exception as e:
        logging.error("Object list query failed...\n")
        raise e
    return res


def view_qry(coll):
    project_qry = {
        "_id": 0,
        "vi": 1,
        "alias": 1
    }
    try:
        # res = list(coll.find({},project_qry))
        res = coll.find({},project_qry)
        # logging.debug("View list document count : {0}".format(len(res)))
    except Exception as e:
        logging.error("View list query failed...\n")
        raise e
    return res


@timed
def make_session_event_backup(client, fromDt, toDt):
    """
    :param client: MongoDB Client
    :param fromDt: ex) "2022-01-01T00:00:00"
    :param toDt: ex) "2022-01-01T00:00:00"
    :return: void
    """
    try:
        target_DB = client.get_database("userhabit")
        session_coll = target_DB.get_collection("session")
    except Exception as e:
        logging.error(f"BACKUP Fail - Mongodb Module Error: {0}".format(e))
        exit(1)

    logging.info(f"BACKUP, From: {fromDt} To: {toDt}")

    """ Object & View List File Create """
    try:
        object_coll = target_DB.get_collection("object_list_pt24h")
        view_coll = target_DB.get_collection("view_list_pt24h")

        object_list = object_qry(object_coll)
        view_list = view_qry(view_coll)

        create_dump_file(object_list, "Mongo_Object_List_", "w")
        create_dump_file(view_list, "Mongo_View_List_", "w")
    except Exception as e:
        logging.debug("Dump Failed from object, view list: {0}\n".format(e))
        raise e

    """ Session Event List File Create """
    pips = [
        {
            "$match": {
                "st": {
                    "$gte": datetime.datetime.strptime(fromDt, "%Y-%m-%dT%H:%M:%S"),
                    "$lt": datetime.datetime.strptime(toDt, "%Y-%m-%dT%H:%M:%S")
                },
            }
        },
        {
            "$lookup": {
                "from": "event",
                "localField": "_id",
                "foreignField": "_id.si",
                "as": "event"
            }
        },
        {
            "$limit": 100000
        },
        # {
        #     "$count": "Total_Document_Count"
        # },
    ]

    # try:
    #     docs_cnt = list(session_coll.aggregate(pipeline=pips)).pop()
    #     logging.debug(f"{docs_cnt}")
    #     if docs_cnt["Total_Document_Count"] >= 1000000:
    #         logging.warning("Data Size Is too much")
    #     pips.pop()
    # except IndexError as e:
    #     logging.debug("Document is empty. BACKUP END.\n")
    #     exit(1)

    try:
        # docs = list(session_coll.aggregate(pipeline=pips))
        docs = session_coll.aggregate(pipeline=pips)
        create_dump_file(docs, "Mongo_Raw_Data_", "w")
    except Exception as e:
        logging.error("Aggregate Error => {0}".format(e))
        exit(1)


if __name__ == '__main__':
    # mceadm/data/ *.log
    logging.basicConfig(filename="{path}{log_name}".format(path=LOG_PATH, log_name="mongoDump.log"),
                        level=logging.DEBUG,
                        format="%(levelname)s:%(asctime)s:%(message)s", )
    config_exception = DumpException()
    if not config_exception.res:
        logging.error("Please checked configuration file.")
        exit(1)
    if sys.argv[1] == "--help":
        # raise ValueError("CLI Format: mongodb://{ID}:{PW}@{HOST}:{PORT} {BOOL} {TO DATE} {FROM DATE}")
        raise ValueError("CLI Format: {BOOL} {TO DATE} {FROM DATE}")
    try:
        now = sys.argv[1]
        if now != "true" and now != "True":
            from_date = sys.argv[1]
            to_date = sys.argv[2]
        elif now == "true" or now == "True":
            from_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%dT00:00:00")
            to_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%dT23:59:59")
    except Exception as e:
        logging.error("Invalid Parameter. please checked date. ( ex: 2022-01-01T00:00:00 )")
        exit(1)
    try:
        client = pymongo.MongoClient(MONGO_ADDRESS)
    except Exception as e:
        logging.error("Time out. Please checked Address and Port\n", e)
        exit(1)
    # make_backup(client, "2022-01-01T00:00:00", "2022-12-31T00:00:00") # Debug
    make_session_event_backup(client, from_date, to_date)