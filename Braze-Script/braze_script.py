import asyncio
import datetime
import multiprocessing
import json
import os

import aiohttp
import aiomysql
import time
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


async def test_braze_api():
    headers = {
        "Authorization": os.getenv("BRAZE_REST_API_KEY")
    }

    body = [{
        'external_id': 563957,
        'sex': 'm',
        'is_sms_target': 'n',
        'is_email_target': 'n',
        'is_push_target': 'n',
        'is_deleted': 'n',
        'favorite_brands': ["Ami", "Fear of God", "Wooyoungmi"],
        'sms': None,
        'app_push': None,
        'brandcode': None,
        'brandnm': None,
        'brandnm_kr': None
    }]

    res = requests.post(
            os.getenv("BRAZE_INSTANCE"),
            headers=headers,
            json={
              "attributes": body
            }
        )
    print(json.loads(res.content.decode("utf-8")))


async def execute_braze(data):
    print("\nExecuting Braze api...")
    headers = {
        "Authorization": os.getenv("BRAZE_REST_API_KEY")
    }
    header = [
        "external_id",
        "is_sms_target",
        "is_email_target",
        "is_push_target",
        "is_deleted",
        "favorite_brands"
    ]
    data = [
        {
            header[i]: int(row[i]) if i == 0 else row[i]
            if i != 5 else row[i].split(",")
            if i == 5 and row[i] is not None else []
            for i in range(0, len(row))
        } for row in data
    ]

    data = [
        {
            **item,
            'sms': None,
            'app_push': None,
            "brandcode": None,
            "brandnm": None,
            "brandnm_kr": None
        } for item in data
    ]

    if len(data) != 0:
        print("Data: ", data[-1], len(data))
    else:
        return

    """ 
        스크립트 동작을 보니 response을 받는데 걸리는 속도가 길다.
        http requets의 응답을 비동기로 처리하면 성능적인 측면에서는
        좋아지겠지만, 해당 api 처리 여부의 무결성을 체크하기 어렵다.
    """
    res = requests.post(
        os.getenv("BRAZE_INSTANCE"),
        headers=headers,
        json={
          "attributes": data
        }
    )
    print(json.loads(res.content.decode("utf-8")))
    # async with session.post(os.getenv("BRAZE_INSTANCE"), headers=headers, json={"attributes": data}) as response:
    #     # 응답 처리 로직
    #     print("Braze Res:", await response.json())


async def create_pool():
    return await aiomysql.create_pool(
            host=os.getenv("INTERNAL_DB_HOST"),
            port=int(os.getenv("INTERNAL_DB_PORT")),
            user=os.getenv("INTERNAL_DB_USER"),
            password=os.getenv("INTERNAL_DB_PWD"),
            db=os.getenv("INTERNAL_DB"),
            autocommit=True,
            minsize=1,
            maxsize=10
        )


async def fetch_member():
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                select u.m_no,
                       u.sms as is_sms_target,
                       u.mailling as is_email_target,
                       u.app_push as is_push_target,
                       u.is_delete,
                        group_concat(
                            (
                                select brandnm
                                from gd_goods_brand b
                                where bdw.brandno = b.sno
                
                            )
                       ) as favorite_brands
                from (
                    select m.m_no,
                           m.sms,
                           m.mailling,
                           m.app_push,
                           'n' as is_delete
                    from gd_member m
                    union
                    select h.m_no,
                           'n' as sms,
                           'n' as mailling,
                           'n' as app_push,
                           'y' as is_delete
                    from gd_log_hack h
                ) as u
                    left join bl_designer_wish bdw
                        on u.m_no = bdw.m_no
                group by u.m_no;
                """)
            data = await cur.fetchall()
            if data is None:
                print("DB is Empty !!")
                return False
            # print(f"DB Count: {len(data)}, \n Ex.[0]: {list(data[0])}\n Ex.[-1]: {list(data[-1])}")
            data = [tuple(item if item != '' else 'n' for item in row) for row in data]
            return data


async def run_tasks(data):  # session, aiohttp
    """
    Braze track api execute
    :param data: internal db document
    """
    await execute_braze(data)


async def number_of_member_all():
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                SELECT count(*)
                from godomall.gd_member
                """)
            data = await cur.fetchone()
            if data is None:
                return False
            print(f"DB Count: {data[0]}")
            return data[0]


async def main():
    print("Braze Script Start: ", datetime.datetime.now())
    st = time.time()
    # await test_braze_api()

    # 내부 DB 데이터 fetch
    result = await fetch_member()
    if result is False: raise "Braze Script Fail, Document is zero."

    # 프로세스 개수
    num_processes = multiprocessing.cpu_count()
    # total_member_cnt = await number_of_member_all()

    mt = time.time()

    # 각 프로세스에서 처리할 범위
    chunk_size = 50  # 1 ap is 75 attributes => 50
    total_numbers = len(result)
    # total_numbers = 750001
    # 비동기 작업 리스트
    tasks = []
    print(f"Total: {total_numbers}\nStart Offset: {result[0]}\nLast Offset: {result[-1]}")
    print(f"Fetch Time: {mt - st}")

    # 멀티 프로세스 실행
    with multiprocessing.Pool(processes=num_processes) as pool:
        for i in range(720000, total_numbers + 1, chunk_size):
            start = i
            end = min(i + chunk_size, total_numbers)
            # print(f"Execute: {start} ~ {end}")
            if i % 30000 == 0: await asyncio.sleep(1)
            # 멀티 프로세스로 실행할 함수와 인자 설정
            task = asyncio.create_task(run_tasks(result[start:end]))
            # 비동기 작업 리스트에 추가
            tasks.append(task)
            # await asyncio.sleep(0.1)

    # # aiohttp 세션 생성
    # async with aiohttp.ClientSession() as session:
    #     for i in range(720000, total_numbers + 1, chunk_size):
    #         start = i
    #         end = min(i + chunk_size, total_numbers)
    #         # print(f"Execute: {start} ~ {end}")
    #         if i % 30000 == 0:
    #             await asyncio.sleep(2)
    #
    #         # 비동기 작업 생성
    #         # task = asyncio.create_task(run_tasks(session, result[start:end]))
    #         task = asyncio.create_task(execute_braze(session, result[start:end]))
    #         tasks.append(task)

    # 비동기 작업 완료 대기
    await asyncio.gather(*tasks)
    et = time.time()
    print(f"Process Time: {et - mt}")
    print(f"End Date: {datetime.datetime.now()}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()