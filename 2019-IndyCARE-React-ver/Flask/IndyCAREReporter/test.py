from multiprocessing import Queue, Process
import time, datetime, requests
URL = '127.0.0.1:3000'
SN = 'D1234'


def function_1(q):
    while True:
        s = requests.Session()
        print("Time 1: ", datetime.datetime.now())
        dic = {'mtype': 1, 'msg': 'kpi0', 'mdata': 1}
        s.post(URL + '/reporter/robot/info', json=dic)
        time.sleep(3)


def function_2(q):
    while True:
        s = requests.Session()
        print("Time 2: ", datetime.datetime.now())
        dic = {'mtype': 1, 'msg': 'kpi0', 'mdata': 1}
        s.post(URL + '/reporter/robot/state/' + SN, json=dic)
        
        time.sleep(4)


def function_3(q):
    while True:
        s = requests.Session()
        print("Time 2: ", datetime.datetime.now())
        dic = {'mtype': 1, 'msg': 'kpi0', 'mdata': 1}
        file = ''
        s.post(URL + '/reporter/robot/event/' + file + '/' + SN, json=dic)

        time.sleep(4)


def function_4(q):
    while True:
        s = requests.Session()
        print("Time 2: ", datetime.datetime.now())
        dic = {'mtype': 1, 'msg': 'kpi0', 'mdata': 1}
        s.post(URL + '/reporter/chart/data/' + SN, json=dic)
        
        time.sleep(4)


def function_5(q):
    while True:
        s = requests.Session()
        print("Time 2: ", datetime.datetime.now())
        dic = {'mtype': 1, 'msg': 'kpi0', 'mdata': 1}
        s.post(URL + '/reporter/robot/kpi/' + SN, json=dic)

        time.sleep(4)


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=function_1, args=(q,))
    p2 = Process(target=function_2, args=(q,))
    p3 = Process(target=function_3, args=(q,))
    p4 = Process(target=function_4, args=(q,))
    p5 = Process(target=function_5, args=(q,))
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    p5.join()
    p4.join()
    p3.join()
    p2.join()
    p1.join()
    
    
    
