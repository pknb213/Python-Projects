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
        # 'is_sms_target': 'n',
        # 'is_email_target': 'n',
        # 'is_push_target': 'n',
        # 'is_deleted': 'n',
        # 'favorite_brands': ["Ami", "Fear of God", "Wooyoungmi"],
        # 'sms': None,
        # 'app_push': None,
        # 'brandcode': None,
        # 'brandnm': None,
        # 'brandnm_kr': None
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
            header[i]: int(row[i]) if i == 0 else row[i].split(",") #563957
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

    url = os.getenv("BRAZE_INSTANCE")
    try:
        async with session.post(
                url,
                headers=headers,
                json={"attributes": data},
                ssl=False,
        ) as response:
            # 응답 처리 로직
            # res = response.json()
            # print("\nBraze Res:", res)
            await asyncio.sleep(0.02)
    except aiohttp.ClientConnectorError as e:
        raise f"Connection Error: {str(e)}"


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
    # await test_braze_api()

    # 내부 DB 데이터 fetch
    result = await fetch_member()
    if result is False: raise "Braze Script Fail, Document is zero."

    mt = time.time()

    # 각 프로세스에서 처리할 범위
    chunk_size = 50  # 1 ap is 75 attributes => 50
    total_numbers = len(result)
    # 비동기 작업 리스트
    tasks = set()
    print(f"Total: {total_numbers}\nStart Offset: {result[0]}\nLast Offset: {result[-1]}")
    print(f"Fetch Time: {mt - st}")

    try:
        # aiohttp 세션 생성
        # conn = aiohttp.TCPConnector(limit_per_host=5) # connector=conn 아래 세션 매개변수에 추가 방법
        async with aiohttp.ClientSession() as session: #trust_env=True
            for i in range(0, total_numbers + 1, chunk_size):
                if i % 30000 == 0:
                    await asyncio.sleep(1)
                start = i
                end = min(i + chunk_size, total_numbers)
                # print(f"Execute: {start} ~ {end}")

                # 비동기 작업 생성
                task = asyncio.create_task(execute_braze(session, result[start:end]))
                tasks.add(task)
                await asyncio.sleep(0.02)

            # 비동기 작업 완료 대기
            await asyncio.gather(*tasks) #return_exceptions=True
        await session.close()
    except Exception as e:
        await session.close()
        print("\nError: ", e)
    finally:
        et = time.time()
        print(f"Fetch Time: {mt - st}")
        print(f"Process Time: {et - mt}")
        print(f"End Date: {datetime.datetime.now()}")
        print(f"Total: {total_numbers}\nStart Offset: {result[0]}Last Offset: {result[-1]}")
        return False


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
