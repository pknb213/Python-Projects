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


async def execute_braze(session, data):
    print("\nExecuting Braze api...")
    headers = {
        "Authorization": os.getenv("BRAZE_REST_API_KEY")
    }
    header = [
        "external_id",
        "wishlist_brand"
    ]

    data = [
        {
            header[i]: 563957 if i == 0 else row[i].split(",") # int(row[i])
            if row[i] is not None else []
            for i in range(0, len(row))
        } for row in data
    ]

    data = [
        {
            **item,
            'favorite_brands': None
        } for item in data
    ]

    if len(data) != 0:
        print("Data: ", data, len(data))
    else:
        return

    async with session.post(os.getenv("BRAZE_INSTANCE"), headers=headers, json={"attributes": data}) as response:
        # 응답 처리 로직
        res = await response.json()
        print("\nBraze Res:", res)


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
                        group_concat(
                            (
                                select brandnm
                                from gd_goods_brand b
                                where bdw.brandno = b.sno
                            )
                       ) as wishlist_brand
                from (
                    select m.m_no
                    from gd_member m
                    union
                    select h.m_no
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
            return data


async def run_tasks(session, data):  # session, aiohttp
    """
    Braze track api execute
    :param data: internal db document
    """
    await execute_braze(session, data)


async def main():
    print("Braze Script Start: ", datetime.datetime.now())
    st = time.time()
    try:
        # await test_braze_api()

        # 내부 DB 데이터 fetch
        result = await fetch_member()
        if result is False: raise "Braze Script Fail, Document is zero."

        mt = time.time()

        # 각 프로세스에서 처리할 범위
        chunk_size = 50  # 1 ap is 75 attributes => 50
        total_numbers = len(result)
        total_numbers = 10
        # 비동기 작업 리스트
        tasks = []
        print(f"Total: {total_numbers}\nStart Offset: {result[0]}\nLast Offset: {result[-1]}")
        print(f"Fetch Time: {mt - st}")

        # aiohttp 세션 생성

        for i in range(0, total_numbers + 1, chunk_size):
            session = aiohttp.ClientSession()
            start = i
            end = min(i + chunk_size, total_numbers)
            # print(f"Execute: {start} ~ {end}")
            if i % 30000 == 0:
                await asyncio.sleep(2)

            # 비동기 작업 생성
            # task = asyncio.create_task(run_tasks(session, result[start:end]))
            task = asyncio.create_task(execute_braze(session, result[start:end]))
            tasks.append(task)

        # 비동기 작업 완료 대기
        await asyncio.gather(*tasks)
    except Exception as e:
        print("\nError: ", e)
    finally:
        et = time.time()
        print(f"Fetch Time: {mt - st}")
        print(f"Process Time: {et - mt}")
        print(f"End Date: {datetime.datetime.now()}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
