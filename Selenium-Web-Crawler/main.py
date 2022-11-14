import asyncio
import pprint
import sys
sys.path.append("./")
from multiprocessing import cpu_count
from timeit import default_timer as timer
from datetime import timedelta
from shop_class import Gmarket, Gsshop

if __name__ == '__main__':
    et = timer()
    pp = pprint.PrettyPrinter(indent=4)
    num_cores = cpu_count()
    print("My Cores Num : ", num_cores)
    gmarket = Gmarket()
    gsshop = Gsshop()
    loop = asyncio.get_event_loop()
    extract_gmarket_list = loop.run_until_complete(gmarket.main())
    extract_gsshop_list = loop.run_until_complete(gsshop.main())
    gmarket_data = []
    gsshop_data = []
    [gmarket_data.extend(extract_gmarket_list[i]) for i in range(len(extract_gmarket_list))]
    [gsshop_data.extend(extract_gsshop_list[i]) for i in range(len(extract_gsshop_list))]
    print("Count : Gmarket({0}), GSshop({1}".format(len(gmarket_data), len(gsshop_data)))
    print("Extract 시간 :", timedelta(seconds=timer() - et))
    it = timer()
    r = loop.run_until_complete(gmarket.insert(gmarket_data))
    r2 = loop.run_until_complete(gsshop.insert(gsshop_data))
    loop.close()
    print("Insert 시간", timedelta(seconds=timer() - it))