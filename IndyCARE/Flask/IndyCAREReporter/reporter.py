import sys, os
from multiprocessing import Process
# sys.path.append(os.getcwd() + os.path.sep + 'reporter_conf')
# print(os.getcwd() + os.path.sep + 'reporter_conf')
sys.path.append('/home/user/release/IndyCAREReporter/reporter_conf')
from config import URL, SITE, COMPANY, HEADER, MODEL
from http_conf import URL, SSEClient
from util_conf import requests, Process, Queue, set_start_method, random, datetime, time, MessageQueue, O_CREAT, \
    set_proc_name, check_robot_info, check_shm, check_task_manager, json
from event_conf import EventFiles
from indyShm_conf import *
from reporterShm_conf import *

SIMULATION = False
ROBOT_SERIAL_NUMBER = 'D1234'


def show_reporter_info():
    print("\n*********** Reporter Information *************")
    print("> OS Basic Path : %s" % os.getcwd())


# Test Process : Default is False
def test_process(sn='D1234'):
    # todo : Test
    s = requests.Session()
    i = 0
    while True:
        try:
            dic = {'mtype': 1, 'msg': 'kpi0', 'mdata': 1}
            s.post(URL + '/opdata/' + sn, json=dic)
            time.sleep(1)
            dic = {'mtype': 2, 'msg': 'kpi1',
                   'mdata': str(random.randrange(20.0, 50.0)) + ',' + str(random.randrange(20.0, 50.0)) + ',' + str(
                       random.randrange(20.0, 50.0)) + ',' + str(random.randrange(20.0, 50.0)) + ',' + str(
                       random.randrange(20.0, 50.0)) + ',' + str(random.randrange(20.0, 50.0))}
            s.post(URL + '/opdata/' + sn, json=dic)
            dic = {'busy': random.randrange(0, 2), 'ready': random.randrange(0, 2), 'collision': random.randrange(0, 2),
                   'emergency': random.randrange(0, 2), 'error': random.randrange(0, 2),
                   'program_state': random.randrange(0, 2),
                   'isServerConnected': random.randrange(0, 2), 'isReporterRunning': random.randrange(0, 3)}
            s.post(URL + '/report/robot/state/' + sn, json=dic)
            dic = {'mtype': 2, 'msg': 'kpi2', 'mdata': random.randrange(10, 50)}
            s.post(URL + '/opdata/' + sn, json=dic)
        except requests.exceptions.ConnectionError:
            t1 = t0 = datetime.datetime.now()
            print("Connect Error !!")
            while True:
                print("Reconnected . . . ", t1.timestamp() - t0.timestamp())
                try:
                    res = s.post(URL + '/opdata', json={"x": str(datetime.datetime.now()), "y": 777}, timeout=15)
                    if res.status_code == 200:
                        break
                except requests.exceptions.RequestException:
                    time.sleep(5)
                if t1.timestamp() - t0.timestamp() > 60:
                    print("<P4> Session ReConnected")
                    s.close()
                    time.sleep(1)
                    s = requests.Session()
                    t0 = datetime.datetime.now()
                t1 = datetime.datetime.now()
        time.sleep(5)
        i += 1


def task_server(q, sn):
    print("Task Server Start")
    # 0o666
    mq = MessageQueue(POSIX_MSG_QUEUE, flags=O_CREAT, mode=0o666, max_messages=100, max_message_size=1024)
    msg_counter = MessageCounter(MSG_COUNTER_SHM, 0, 4)
    while mq.current_messages > 0:
        try:
            mq.receive()
        except KeyboardInterrupt:
            print("> Task Server Signal Exit")
            sys.exit()

    while True:
        t0 = datetime.datetime.now()
        try:
            msg_counter.inc()
            data, pri = mq.receive()
        except KeyboardInterrupt:
            print("> Task Server Signal Exit")
            while mq.current_messages > 0:
                print('> flush')
                mq.receive()
            sys.exit()
        except:
            print("> Task exception")
            while mq.current_messages > 0:
                print('> flush')
                mq.receive()
            sys.exit()

        t1 = datetime.datetime.now()
        # print("> Queue Delay : ", t1 - t0, t1.timestamp() - t0.timestamp())
        mtype, len = unpack('ll', data[:8])  # long is 4 byte ( mtype = 4, len = 4 )
        # print("type : ", type(data), " len : ", len, " pri : ", pri)
        msg = data[8:8 + data[8:].index(0)].decode('utf-8')  # 8부터 처음 0 나올 때 까지
        mdata = data[136:136 + data[136:].index(0)].decode('utf-8')  # 8 + 128 부터 0 나올 때 까지
        print("> mtype [%s]" % mtype, ", msg [%s]" % msg, ", mdata [%s]" % mdata, ", msg counter [%s]" % msg_counter.counter)

        try:
            q.put_nowait((mtype, msg, mdata))
        except KeyboardInterrupt:
            print("> Task Server Signal Exit")
            sys.exit()
        except Exception as e:
            print("> Exception Queue :", e)
            while mq.current_messages > 0:
                print('> flush')
                mq.receive()
            time.sleep(5)
            continue


def reporter(q, sn, shm):
    while True:
        try:
            # Create SHM Object
            error_shm = ErrorCode(INDY_SHM, INDY_SHM_ROBOT_CTRL_STATUS_ADDR, ROBOT_CTRL_STATUS_SHM_SIZE)
            robot_shm = RobotState(INDY_SHM, INDY_SHM_ROBOT_STATE_ADDR, ROBOT_STATE_SHM_SIZE)
            ctrl_shme = ControlState(INDY_SHM, INDY_SHM_ROBOT_CTRL_STATUS_ADDR, ROBOT_CTRL_STATUS_SHM_SIZE)
            # info_shm = RobotInfoData(INDY_SHM, INDY_SHM_ROBOT_INFO_ADDR, ROBOT_INFO_SHM_SIZE)
            reporter_shm = ReporterState(INDY_SHM, INDY_SHM_REPORTER_STATE_ADDR, REPORTER_STATE_SHM_SIZE)
            # sys_shm = SystemState(NRMK_SHM, NRMK_SHM_SYSTEM_ADDR, SYSTEM_SHM_SIZE)
        except Exception as e:
            print("\n Reporter Execution Fail : ", e)
            time.sleep(5)
        else:
            break

    while True:
        s = requests.Session()
        # s.post(URL + '/login', {'id': sn, 'pwd': sn})
        t0 = datetime.datetime.now()
        # todo : About CONTY Alert
        reporter_shm.turn_on_reporter(reporter_shm)
        reporter_shm.turn_on_server(reporter_shm)
        # Todo : First, Session Check. Second, Queue Receive. Third, Post the Status.
        # Todo : Session Check
        try:
            while q.qsize() > 0:
                mtype, msg, mdata = q.get()
                if mtype == 1:
                    print("Received Count( %s %s )" % (mtype, msg))
                    dic = {'mtype': mtype, 'msg': msg, 'mdata': mdata}
                    s.post(URL + '/reporter/chart/data/' + sn, json=dic)
                    # s.post(URL + '/opdata/' + sn, json=dic)
                    # POST(s, '/report_robot_opdata/' + sn, json=json.dumps({msg: 1.0}))
                elif mtype == 2:
                    print("Received Mean( %d %s %s )" % (mtype, msg, mdata))
                    dic = {'mtype': mtype, 'msg': msg, 'mdata': mdata}
                    s.post(URL + '/reporter/chart/data/' + sn, json=dic)
                    # s.post(URL + '/opdata/' + sn, json=dic)
                    # POST(s, '/report_robot_opdata/' + sn, json=json.dumps(_dic))
                elif mtype == 100:
                    # {'mtype': 100, 'mdata': 'kpi1,tt,hour,mean,6', 'msg': 'kpi_config'}
                    print("KPI configuration( %s, %s )" % (msg, mdata))
                    dic = {'mtype': mtype, 'msg': msg, 'mdata': mdata}
                    s.post(URL + "/reporter/robot/kpi/" + sn, json=dic)
                    # POST(s, '/report_kpi_string/' + sn, json=json.dumps({msg: mdata}))
                else:
                    pass
            # Todo : Reporter State Check
            state_idc = {}
            state_idc.update(error_shm.get_all_error(error_shm))
            state_idc.update(robot_shm.get_all_state(robot_shm))
            state_idc.update(ctrl_shme.get_all_robot_state(ctrl_shme))
            # state_idc.update(info_shm.get_all_robot_info_data(info_shm))
            state_idc.update(reporter_shm.get_all_reporter_state(reporter_shm))
            # state_idc.update(sys_shm.get_all_sys_state(sys_shm))
            s.post(URL + '/reporter/robot/state/' + sn, json=json.dumps(state_idc))

            print("\nReporter : ", t0, shm.get_all_reporter_state(shm))
            print(state_idc, "\n")
            if EventFiles.check_if_new_log():
                log_file = EventFiles.latest_log[len(EventFiles.EVENT_DIRECTORY):]
                print("Update Log File : ", log_file)
                # 여기서 바로 file로 event log를 보내도 된다고 생각 함
                date = str(datetime.datetime.strptime(log_file[12:-4], '%m-%d-%Y-%H-%M-%S'))
                code = int(log_file[:2])
                print(date, code)
                s.post(URL + '/reporter/robot/event/' + sn, json={"time": date, "code": code, "log": EventFiles.latest_log})
            s.close()
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("> Reporter Signal Exit")
            s.close()
            sys.exit()
        except requests.exceptions.ConnectionError as e:
            t1 = t0 = datetime.datetime.now()
            print("> Reporter Connect Error !!", e)
            while True:
                print("<Reporter> Reconnecting . . . ", t1.timestamp() - t0.timestamp())
                try:
                    res = s.get(URL + '/ping', timeout=9)
                    print("Ping res :", res)
                    if res.status_code == 200:
                        print("<Reporter> Reconnected - ", end=' ')
                        break
                    elif res.status_code == 404:
                        s.close()
                        time.sleep(5)
                        s = requests.Session()
                except requests.exceptions.ConnectionError:
                    time.sleep(1)
                except KeyboardInterrupt:
                    print("> Reporter Signal Exit")
                    s.close()
                    sys.exit()
                except Exception as e:
                    print(e)
                    time.sleep(2)
                if t1.timestamp() - t0.timestamp() > 60:
                    print("<Reporter> Session Time Over")
                    s.close()
                    time.sleep(1)
                    s = requests.Session()
                    t0 = datetime.datetime.now()
                t1 = datetime.datetime.now()
            s.close()
            time.sleep(1)
            continue
        except Exception as e:
            print("<Reporter Exception !> ", e)
            s.close()
            time.sleep(2)
            continue


def event_log_uploader(sn, shm):
    while True:
        print("Event Log Uploader Start")
        s = requests.Session()
        # s.post(URL + '/login', {'id': sn, 'pwd': sn})
        try:
            messages = SSEClient(URL + '/stream?channel=%s_event_log' % sn)
        except KeyboardInterrupt:
            print("> Event Log Signal Exit")
            s.close()
            sys.exit()
        except requests.exceptions.ConnectionError as e:
            t1 = t0 = datetime.datetime.now()
            print("> Log Connect Error !!", e)
            while True:
                print("<Event> Reconnecting . . . ", t1.timestamp() - t0.timestamp())
                try:
                    res = s.get(URL + '/ping', timeout=9)
                    if res.status_code == 200:
                        print("<Event> Reconnected - ", end=' ')
                        break
                    elif res.status_code == 404:
                        s.close()
                        time.sleep(5)
                        s = requests.Session()
                except requests.exceptions.ConnectionError:
                    time.sleep(1)
                except KeyboardInterrupt:
                    print("> Event Log Signal Exit")
                    s.close()
                    sys.exit()
                except Exception as e:
                    print(e)
                    time.sleep(2)
                if t1.timestamp() - t0.timestamp() > 60:
                    print("<Event> Session Time Over")
                    s.close()
                    time.sleep(1)
                    s = requests.Session()
                    t0 = datetime.datetime.now()
                t1 = datetime.datetime.now()
            s.close()
            time.sleep(1)
            continue
        except Exception as e:
            print("> SSE Exception e : ", e)
            s.close()
            time.sleep(1)
            continue
        try:
            for msg in messages:
                print("<Events> msg : ", msg.data)
                data = json.loads(msg.data)
                if EventFiles.get_directory_path():
                    with open(EventFiles.get_directory_path() + data['filename'], 'rb') as f:
                        print(f)
                        try:
                            res = s.post(URL + '/datatable/event/%s/%s'
                                         % (data['filename'], data['sn']), files={'file': f})
                        except requests.exceptions.ConnectionError:
                            t1 = t0 = datetime.datetime.now()
                            while True:
                                print("<Events> Reconnecting . . . ", t1.timestamp() - t0.timestamp())
                                try:
                                    if EventFiles.get_directory_path():
                                        with open(EventFiles.get_directory_path() + data['filename'], 'rb') as f:
                                            print(f)
                                            res = s.post(URL + '/datatable/event/%s/%s' % (data['filename'], data['sn']),
                                                         files={'file': f})
                                        if res.status_code == 200:
                                            print("<Events> Reconnected !!")
                                            break
                                except requests.exceptions.ConnectionError:
                                    time.sleep(5)
                                if t1.timestamp() - t0.timestamp() > 60:
                                    print("<Events> Session Time Over")
                                    s.close()
                                    time.sleep(1)
                                    s = requests.Session()
                                    t0 = datetime.datetime.now()
                                t1 = datetime.datetime.now()
        except Exception as e:
            print("<Event Exception !> ", e)
            s.close()
            time.sleep(2)
            continue


def clip_uploader(sn, shm):
    while True:
        print("Clip Uploader Start ( %s )" % EventFiles.EVENT_DIRECTORY)
        s = requests.Session()
        # s.post(URL + '/login', {'id': sn, 'pwd': sn})
        try:
            messages = SSEClient(URL + '/stream?channel=%s_clip' % sn)
        except KeyboardInterrupt:
            print("> Clip Uploader Signal Exit")
            s.close()
            sys.exit()
        except requests.exceptions.ConnectionError as e:
            print("> Clip Connect Error !!", e)
            t1 = t0 = datetime.datetime.now()
            while True:
                print("<Clip> Reconnecting . . . ", t1.timestamp() - t0.timestamp())
                try:
                    res = s.get(URL + '/ping', timeout=9)
                    if res.status_code == 200:
                        print("<Clip> Reconnected - ", end=' ')
                        break
                    elif res.status_code == 404:
                        s.close()
                        time.sleep(5)
                        s = requests.Session()
                except requests.exceptions.ConnectionError:
                    time.sleep(1)
                except KeyboardInterrupt:
                    print("> Clip Uploader Signal Exit")
                    s.close()
                    sys.exit()
                except Exception as e:
                    print(e)
                    time.sleep(2)
                if t1.timestamp() - t0.timestamp() > 60:
                    print("<Clip> Session Time Over")
                    s.close()
                    time.sleep(1)
                    s = requests.Session()
                    t0 = datetime.datetime.now()
                t1 = datetime.datetime.now()
            s.close()
            time.sleep(1)
            continue
        try:
            for msg in messages:
                print("<Clip> msg : ", msg)
                if EventFiles.get_latest_clip():
                    with open(EventFiles.get_latest_clip(), 'rb') as f:
                        print(f)
                        res = s.post(URL + '/reporter/robot/clip/' + sn, files={'file': f})
                else:
                    print("No Clip")
                    res = s.post(URL + '/reporter/robot/clip/' + sn, files={'file': ('No Camera', '')})
        except requests.exceptions.ConnectionError as e:
            t1 = t0 = datetime.datetime.now()
            print("-- Connect Error !!", e)
            while True:
                print("<Clip> Reconnecting . . . ", t1.timestamp() - t0.timestamp())
                try:
                    if EventFiles.get_latest_clip():
                        with open(EventFiles.get_latest_clip(), 'rb') as f:
                            res = s.post(URL + '/reporter/robot/clip/' + sn, files={'file': f})
                    else:
                        res = s.post(URL + '/reporter/robot/clip/' + sn, files={'file': ('No Camera', '')})
                    if res.status_code == 200:
                        print("<Clip> Reconnected !!")
                        break
                except requests.exceptions.ConnectionError:
                    time.sleep(5)
                if t1.timestamp() - t0.timestamp() > 60:
                    print("<Clip> Session Time Out")
                    s.close()
                    time.sleep(1)
                    s = requests.Session()
                    t0 = datetime.datetime.now()
                t1 = datetime.datetime.now()
        except Exception as e:
            print("<Event Exception !> ", e)
            s.close()
            time.sleep(2)
            continue


if __name__ == '__main__':
    set_start_method('spawn', True)
    shm = ReporterProcessState(REPORTER_PROCESS_SHM, REPORTER_PROCESS_STATE_ADDR, REPORTER_PROCESS_SHM_SIZE)
    print(" >> URL : %s, Company : %s, Site : %s, Header : %s, Model : %s" % (URL, COMPANY, SITE, HEADER, MODEL))
    if SIMULATION:
        while True:
            s = requests.Session()
            try:
                s.post(URL + '/reporter/robot/info', json={'sn': ROBOT_SERIAL_NUMBER, 'company': COMPANY, 'site': SITE, 'header': HEADER, 'model': MODEL})
            except Exception as e:
                print("> Post Error. Please Check the URL & Server : ", e)
                s.close()
                time.sleep(5)
                continue
            break
    else:
        while True:
            f1 = check_task_manager()
            f2 = check_shm()
            sn = check_robot_info()
            shm.write_serial_number(shm, sn)
            ROBOT_SERIAL_NUMBER = sn
            print("Robot SerialNumber : ", shm.get_serial_number_value(shm))
            if f1 is True and f2 is True and sn:
                s = requests.Session()
                try:
                    s.post(URL + '/reporter/robot/info', json={'sn': ROBOT_SERIAL_NUMBER, 'company': COMPANY, 'site': SITE, 'header': HEADER})
                    time.sleep(0.5)
                    s.close()
                    time.sleep(1.5)
                except Exception as e:
                    print("\n> Post Error. Please Check the URL & Server : ", e)
                    time.sleep(5)
                    continue
                break

    show_reporter_info()
    q = Queue()
    p1 = Process(target=event_log_uploader, args=(ROBOT_SERIAL_NUMBER, shm,))
    p2 = Process(target=clip_uploader, args=(ROBOT_SERIAL_NUMBER, shm,))
    p3 = Process(target=task_server, args=(q, ROBOT_SERIAL_NUMBER,))
    # p4 = Process(target=test_process, args=(ROBOT_SERIAL_NUMBER,))
    p1.start()
    p2.start()
    p3.start()
    # p4.start()
    time.sleep(1)
    reporter(q, ROBOT_SERIAL_NUMBER, shm)
    q.close()
    q.join_thread()
    # p4.join()
    p3.join()
    p2.join()
    p1.join()
