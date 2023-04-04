import asyncio
import csv
import json
import logging
import os
import aiofiles
import aiomysql
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')


KAKAO_ADMIN_KEY = os.getenv("KAKAO_ADMIN_KEY")


async def create_doc_for_mariadb(_dic):
    """
    KakaoSync 데이터 Key, Value 추출
    :param _dic: KakaoSync Dict
    """
    if "allowed_service_terms" not in _dic: return {"m_id": "kakao_{}".format(_dic["user_id"])}
    doc = {"m_id": "kakao_{}".format(_dic["user_id"])}
    list(map(lambda x: doc.update({x["tag"]: x["agreed_at"]}), _dic["allowed_service_terms"]))
    return await key_mapping(doc)


async def key_mapping(_dic):
    """
    KakaoSync와 Internal DB의 Column 명 Mapping
    :param _dic: {Agree Term: Date ...} Dict
    :return: Dict
    """
    res = {"m_id": _dic["m_id"]}
    keys = _dic.keys()
    if "sms" in keys:
        res["sms"] = 'y'
        res["sms_agree_date"] = _dic["sms"]
    else:
        res["sms"] = 'n'
        res["sms_agree_date"] = datetime(1900,1,1,0,0,0).strftime('%Y-%m-%dT%H:%M:%SZ')
    if "email" in keys:
        res['mailling'] = 'y'
        res["mailling_agree_date"] = _dic["email"]
    else:
        res['mailling'] = 'n'
        res["mailling_agree_date"] = datetime(1900,1,1,0,0,0).strftime('%Y-%m-%dT%H:%M:%SZ')
    if "app" in keys:
        res["app_push"] = 'y'
        res["app_push_agree_date"] = _dic["app"]
    else:
        res["app_push"] = 'n'
        res["app_push_agree_date"] = datetime(1900,1,1,0,0,0).strftime('%Y-%m-%dT%H:%M:%SZ')
    if "dm" in keys:
        res["dm"] = 'y'
        res["dm_agree_date"] = _dic["dm"]
    else:
        res["dm"] = 'n'
        res["dm_agree_date"] = datetime(1900,1,1,0,0,0).strftime('%Y-%m-%dT%H:%M:%SZ')
    if "phone" in keys:
        res["tm"] = 'y'
        res["tm_agree_date"] = _dic["phone"]
    else:
        res["tm"] = 'n'
        res["tm_agree_date"] = datetime(1900,1,1,0,0,0).strftime('%Y-%m-%dT%H:%M:%SZ')
    return res


async def get_terms(_id):
    """
    동의한 약관 확인하기
    GET /v1/user/service/terms HTTP/1.1
    Host: kapi.kakao.com
    Authorization: KakaoAK ${APP_ADMIN_KEY}
    :param
        target_id_type: user_id 고정
        target_id: KakaoSync userID
        extra(Option): app_service_terms
    :return:
        user_id: 회원 번호
        allowed_service_terms(Option): 사용자가 동의한 서비스 약관 항목 목록
        app_service_terms(Option): 앱에 사용 설정된 서비스 약관 목록
    """
    # start_time = time.time()
    cnt = 0
    while True:
        try:
            res = requests.get(
                f"https://kapi.kakao.com/v1/user/service/terms?target_id_type=user_id&target_id={_id}&extra=app_service_terms",
                headers={"Authorization": f"KakaoAK {KAKAO_ADMIN_KEY}"})
            _str = res.content.decode("utf-8")
            _dic = json.loads(_str)
            if "code" in _dic:
                # if _dic["code"] == -101:
                #     해당 앱에 카카오계정 연결이 완료되지 않은 사용자가 호출한 경우
                # elif _dic["code"] == -102:
                #     이미 앱과 연결되어 있는 사용자의 토큰으로 연결하기 요청한 경우
                # elif _dic["code"] == -103:
                #     휴면 상태, 또는 존재하지 않는 카카오계정으로 요청한 경우
                _dic = {"user_id": _id}
            doc = await create_doc_for_mariadb(_dic)
            # logging.info(doc)
            if not doc: return {"user_id": _id}
            return doc
        except Exception as e:
            await asyncio.sleep(1)
            logging.info(f"Error get_terms: {e}")
            if cnt <= 5:
                logging.info(f"Error get_terms: Retry more than 5. ID: {_id}\nMessage: {e}")
                return {}
            cnt += 1
            continue
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # logging.info(f">> time: {elapsed_time:.3f} seconds")


async def get_users(from_id):
    """
    사용자 목록 가져오기
    curl -v -X GET "https://kapi.kakao.com/v1/user/ids" \
    -H "Authorization: KakaoAK ${APP_ADMIN_KEY}"
    :param
        limit(Option): 페이지당 사용자 수 (max=100)
        from_id(Option): 페이징 시작 기준이 되는 사용자 회원번호
        order(Option): asc 또는 desc
    :return:
        elements: 회원번호 목록
        before_url(Option): 이전 페이지 URL, 이전 페이지가 없을 경우 null
        after_url(Option): 다음 페이지 URL, 다음 페이지가 없을 경우 null
    """
    url = f"https://kapi.kakao.com/v1/user/ids?from_id={from_id}&order=asc"
    headers = {
        "Authorization": "KakaoAK " + KAKAO_ADMIN_KEY
    }
    logging.info(f"\nStart Get User ID: {from_id} [Data: {datetime.now()}]")
    cnt = 1
    res = []
    while cnt < 11:
        try:
            ids = []
            docs = []
            start_time = time.time()
            if cnt == 0:
                response = requests.get(url, headers=headers)
                decode_res = eval(response.content.decode())
                url = decode_res["after_url"]
                ids.extend(decode_res["elements"])
            else:
                response = requests.get(url, headers=headers)
                try:
                    decode_res = eval(response.content.decode())
                except NameError as e:
                    decode_res = eval(response.content.decode().replace(',"after_url":null', ""))
                    ids.extend(decode_res["elements"])
                    for _id in ids:
                        doc = await get_terms(_id)
                        if doc: docs.append(doc)
                        res.extend(docs)
                    return res
                url = decode_res["after_url"]
                ids.extend(decode_res["elements"])
            for _id in ids:
                doc = await get_terms(_id)
                if doc: docs.append(doc)
            res.extend(docs)
            end_time = time.time()
            logging.info(f"({cnt}) >> 100 rows time: {end_time - start_time:.3f} seconds")
            cnt += 1
        except Exception as e:
            logging.info(f"\nException({cnt})!! Last URL: {url}\n>> {e}")
            await asyncio.sleep(1)
            continue
    return res


async def read_database(_doc, f):
    """
    1. MariaDB에 m_id를 이용하여 과거 데이터 추출.
    2. 해당 데이터를 csv 파일로 라인 추가.
    3. MariaDB에 _dic 값으로 update 실행.
    :table
        godomall.gd_member
    :param
        _doc: Dict
        f: File System Session
    :return:
        Boolean: Not Use
    """
    user = "youngjocheon"
    host = "db-prod-godo.balaan.io"
    pwd = "2074ed93e2360f13788a19020be8447a0279394428925283"
    db = "godomall"

    cnt = 0
    while True:
        try:
            pool = await aiomysql.create_pool(
                host=os.getenv("host"),
                port=int(os.getenv("port")),
                user=os.getenv("user"),
                password=os.getenv("pwd"),
                db=os.getenv("os"),
                autocommit=True,
                minsize=int(os.getenv("min")),
                maxsize=int(os.getenv("max"))
            )

            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(f"""
                            SELECT sms, sms_agree_date, 
                            mailling, mailling_agree_date, 
                            app_push, app_push_agree_date, 
                            dm, dm_agree_date, 
                            tm, tm_agree_date
                            from godomall.gd_member_test
                            WHERE m_id = '{_doc["m_id"]}'
                            """)
                    data = await cur.fetchone()
                    if data is None:
                        return False
                    await cur.execute("""
                        UPDATE godomall.gd_member_test
                        SET sms = '{}', app_push = '{}', dm = '{}', tm = '{}', mailling = '{}',
                            sms_agree_date = '{}', app_push_agree_date = '{}', dm_agree_date = '{}', tm_agree_date = '{}', mailling_agree_date = '{}'
                        WHERE m_id = '{}'
                        """.format(
                        _doc["sms"],
                        _doc["app_push"],
                        _doc["dm"],
                        _doc["tm"],
                        _doc["mailling"],
                        datetime.strptime(_doc["sms_agree_date"], '%Y-%m-%dT%H:%M:%SZ'),
                        datetime.strptime(_doc["app_push_agree_date"], '%Y-%m-%dT%H:%M:%SZ'),
                        datetime.strptime(_doc["dm_agree_date"], '%Y-%m-%dT%H:%M:%SZ'),
                        datetime.strptime(_doc["tm_agree_date"], '%Y-%m-%dT%H:%M:%SZ'),
                        datetime.strptime(_doc["mailling_agree_date"], '%Y-%m-%dT%H:%M:%SZ'),
                        _doc["m_id"]
                        )
                    )
                    if cur.rowcount == 1:
                        await csv.writer(f).writerow(tuple(_doc.values()) + data)
                        await f.flush()
                        # logging.info("!", end="")
                    else:
                        # logging.info(".", end="")
                        pass
            await conn.commit()
            break
        except Exception as e:
            logging.info(f"DB Error: {e}")
            if cnt == 5: return False
            cnt += 1
            await asyncio.sleep(1)
    return True


async def main():
    fields = ["m_id", "kakao_sms", "kakao_sms_agree_date",
              "kakao_mailling", "kakao_mailling_agree_date",
              "kakao_app_push", "kakao_app_push_date",
              "kakao_dm", "kakao_dm_date",
              "kakao_tm", "kakao_tm_date",
              "db_sms", "db_sms_agree_date",
              "db_mailling", "db_mailling_agree_date",
              "db_app_push", "db_app_push_agree_date",
              "db_dm", "db_dm_agree_date",
              "db_tm", "db_tm_agree_date"]
    async with aiofiles.open(f"KakaoSync_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.csv", mode='a', encoding='utf-8', newline='') as f:
        await csv.writer(f).writerow(fields)
        await f.flush()
        from_id = 0
        start_time = time.time()
        while True:
            try:
                documents = await get_users(from_id)
                logging.info(f"Number Of Docs: {len(documents)}")
                if not len(documents):
                    break
                from_id = documents[-1]['m_id'].split('_')[1]
                logging.info(f"Last User ID: {from_id}")
                restore_doc = [i for i in documents if len(i) != 1]
                logging.info(f"Disagree User Del...\nAfter Docs: {len(restore_doc)}")
                if not len(restore_doc): continue
                coroutines = [read_database(doc, f) for doc in restore_doc]
                await asyncio.gather(*coroutines)
            except Exception as e:
                await asyncio.sleep(5)
                logging.info(f"Main Error: {e}\nFrom ID: {from_id}")
        end_time = time.time()
        logging.info(f"Finish - {(end_time - start_time):.3f} seconds")


logging.basicConfig(filename='kakao_sync.log', level=logging.INFO)
# asyncio 이벤트 루프 실행
loop = asyncio.get_event_loop()
loop.run_until_complete(main())