from os import abort

from utils import *
from login import User, login_user, current_user, LoginRequired


# For Login Page
@app.route('/', methods=["POST"])
def home():
    if User.check_user(request.json['email'], request.json['pwd']):
        user = User(request.json['email'])
        login_user(user)
        print("> Login : ", user.id)

        # Todo : 권한에 따른 페이지를 위한 Prams 전달. React에서 랜더링하면 User가 초기화 됨.
        if user.permission == 'user':
            return jsonify('ok')
        else:
            return jsonify("Fail")

    if not current_user.is_authenticated:
        return jsonify("Fail")


# For Robot List Page
@app.route("/datatable/robots/<condition>")
def robots(condition):
    if condition is 'all':
        sql = "SELECT sn, company, site, kpi0, kpi1, kpi2, kpi3, kpi4, model, header FROM robots"
    elif condition is 'developer':
        sql = ""
    elif condition is 'maintainer':
        sql = ""

    sql = "SELECT sn, company, site, kpi0, kpi1, kpi2, kpi3, kpi4, model, header FROM robots"
    res = MySQL.select(sql)
    print(res)
    if res is not None:
        for i in res:
            for k, v in i.items():
                if v is None:
                    i[k] = ''
            robot_state(i['sn'])
            print("Rstate [", i['sn'], "] :", cache.hget(i['sn'], 'state'))
            if not cache.hget(i['sn'], 'state'):
                i['state'] = 0
            else:
                state = eval(cache.hget(i['sn'], 'state').decode())
                if state['error'] or state['collision'] > 0:
                    i['state'] = 2
                elif state['ready'] > 0 or state['busy'] > 0:
                    i['state'] = 1
                else:
                    i['state'] = 0
            i['kpi'] = i['kpi0'] + ', ' + i['kpi1'] + ', ' + i['kpi2'] + ', ' + i['kpi3'] + ', ' + i['kpi4']
            i['enter'] = '<a href=/display/%s>' % i['sn']
            del i['kpi0'], i['kpi1'], i['kpi2'], i['kpi3'], i['kpi4']

    return jsonify(res)


# For Robot Detail Page - State
@app.route("/robot/state/<sn>")
def robot_state(sn):
    # sql = "SELECT state FROM robot_states " \
    #       "WHERE serial_number = \"%s\" AND date >= \"%s\" AND date < \"%s\" " \
    #       "ORDER BY date DESC LIMIT 1 " \
    #       % (sn, (datetime.utcnow() - timedelta(seconds=30)).strftime(fmtAll), datetime.utcnow().strftime(fmtAll))
    # res = MySQL.select(sql, False)
    # print("State Loop Res [%s]: " % sn, res)
    # if res is False:
    #     dic = str({'busy': 0, 'collision': 0, 'emergency': 0, 'error': 0, 'home': 0,
    #                'finish': 0, 'ready': 0, 'resetting': 0, 'zero': 0, 'is_server_connected': 1})
    #     cache.hset(sn, 'state', dic)
    #     return jsonify(dic)
    #
    # cache.hset(sn, 'state', res['state'])

    # return jsonify(res['state'])

    # Todo : 캐시에 저장된 로봇 상태값을 가져온다
    # Todo : 지금은 Static 값으로 테스트 한다.
    # dic = cache.hget(sn, 'state').decode('utf8')
    #
    # dic = {'busy': random.randrange(0, 2), 'ready': random.randrange(0, 2), 'collision': random.randrange(0, 2),
    #        'error': random.randrange(0, 2), 'program_state': random.randrange(0, 2), 'emergency': random.randrange(0, 2),
    #        'is_reporter_running': random.randrange(0, 2), 'is_server_connected': random.randrange(0, 2)}
    # cache.hset(sn, 'state', str(dic))
    if cache.hget(sn, 'state') is not None:
        _state = json.loads(cache.hget(sn, 'state').decode())
        dic = _state
        # print(_state)
    else:
        dic = {}
    return jsonify(dic)


# For Robot Detail Page - Events
@app.route("/datatable/events/<sn>/<condition>")
def events(sn, condition):
    if condition == 'all':
        sql = "SELECT idx, json, file, sn, " \
              "DATE_FORMAT(CONVERT_TZ(occurrence_time, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%s') " \
              "as occurrence_time " \
              "FROM events " \
              "WHERE sn=\"%s\" ORDER BY occurrence_time DESC " % sn
    else:
        sql = "SELECT idx, json, file, sn, " \
              "DATE_FORMAT(CONVERT_TZ(occurrence_time, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%s') " \
              "as occurrence_time " \
              "FROM events " \
              "WHERE sn=\"%s\" ORDER BY occurrence_time DESC LIMIT 5 " % sn
    res = MySQL.select(sql, True)

    if not res: return jsonify('')
    for i in res:
        if not i['json']: del i
        a = i['json'].replace("\'", "\"")
        a = a.replace("\\", "\\\\")
        a = json.loads(a)
        i['code'] = get_robot_code_description(a['code'])
        # a = a['log'].split('\\')  # For Window
        a = a['log'].split('/')  # For Linux
        i['down'] = '<a class=c_hyper href=http://121.67.47.157:8884/datatable/event/%s/%s>' % (a[-1], i['sn'])

    return jsonify(res)


# For Robot Detail Page - Events
@app.route("/datatable/event/<filename>/<sn>", methods=["GET", "POST"])
def request_event(filename, sn):
    print(filename, sn, request)
    clip_path = os.path.join(os.getcwd(), 'upload')
    if request.method == "GET":
        cache.hset(sn, 'event_log', 0)
        print("Log를 요청하겠사와요")
        load_sse_command(sn, '_event_log', {'sn': sn, 'filename': filename})
    elif request.method == "POST":
        if request.files:
            file_name = request.files['file'].filename
            request.files['file'].save(os.path.join(clip_path, file_name))
            cache.hset(sn, 'event_log', 1)
            cache.hset(sn, 'log_name', file_name)
            return Response('ok')
        else:
            return Response("Empty the File", status=404)
    else:
        return Response("Undefined Http Method Type")
    t1 = t0 = datetime.now()
    while t1.timestamp() - t0.timestamp() <= app.config['ROBOT_DATA_WAIT_TIMEOUT']:
        st = int(cache.hget(sn, 'event_log'))
        if st < 0:
            print("Fail")
            return Response("No Log", status=404)
        if st > 0:
            res = send_from_directory(clip_path, cache.hget(sn, 'log_name').decode('utf-8'),
                                      as_attachment=True,
                                      attachment_filename=cache.hget(sn, 'log_name').decode('utf-8'))
            print("Succ :", res)
            print(cache.hgetall(sn))
            return res

        time.sleep(1)
        t1 = datetime.now()
        print('Log Waiting', t1.timestamp() - t0.timestamp())

    return redirect('http://indycare.neuromeka.com:8883/display/' + sn)


# For Robot Detail Page - Video
@app.route("/clip/<sn>")
def cam(sn):
    # print(os.path.join(os.getcwd(), 'upload'))
    # path = os.path.join(os.getcwd(), 'upload')
    # res = send_from_directory(path, 'Chronograf.mp4')
    # res = send_from_directory(path, b'video-11-26-2019-19-22-36.mp4'.decode())
    # return res

    # Todo : Clip 요청하는 코드 작성 필요
    t0 = t1 = datetime.now()
    print("처음임" if cache.hget(sn, 'clip') is None else "Clip 값 : ", cache.hget(sn, 'clip'))
    if cache.hget(sn, 'clip') is None or float(cache.hget(sn, 'clip')) < 0:
        cache.hset(sn, 'clip', 0)
        print("Clip 요청을 하옵니다")
        load_sse_command(sn, '_clip')
        cache.hset(sn, 'clip_ts', datetime.now().timestamp())

    print('영상 ts 없뜸' if cache.hget(sn, 'clip_ts') is None else 'now - clip_ts : %f' % (
                t0.timestamp() - float(cache.hget(sn, 'clip_ts'))))
    while t1.timestamp() - t0.timestamp() <= app.config['ROBOT_DATA_WAIT_TIMEOUT']:
        if cache.hget(sn, 'clip_ts') is not None \
                and datetime.now().timestamp() - float(cache.hget(sn, 'clip_ts')) > 60:
            print("오래됬으니 다시 요청하세요")
            cache.hset(sn, 'clip', -1)
            cache.hdel(sn, 'clip_ts')
            return 'fail'
        if float(cache.hget(sn, 'clip')) > 0:
            print("영상 받음", cache.hget(sn, 'clip'), cache.hget(sn, 'clip_name').decode())
            return 'ok'
        elif float(cache.hget(sn, 'clip')) < 0:
            return 'fail'
        t1 = datetime.now()
        print("waiting. . ", t1.timestamp() - t0.timestamp())
        time.sleep(2)

    if cache.hget(sn, 'clip') is 0:
        cache.hset(sn, 'clip', -1)
    return 'fail'


# For Robot Detail Page - Video
@app.route("/get/poster")
def get_poster():
    return send_from_directory(os.path.join(os.getcwd(), 'static/img'), 'video_loading.jpg')


# For Robot Detail Page - Video
@app.route("/get/clip/<sn>")
def get_clip(sn):
    print("GET CLIP")
    path = os.path.join(os.getcwd(), 'upload')
    try:
        return send_from_directory(path, cache.hget(sn, 'clip_name').decode())
    except FileNotFoundError:
        return Response("File Not Found", status=404)


# For Robot Detail Page - Chart
@app.route("/get/kpi/<sn>")
def get_kpi(sn):
    sql = "SELECT kpi0, kpi1, kpi2, kpi3, kpi4 FROM robots WHERE sn = \"%s\" " % sn
    kpi_str = MySQL.select(sql, False)
    print("KPI RES : ", kpi_str)
    if not kpi_str: return jsonify('')
    res = []
    for k, v in kpi_str.items():
        if v is not None:
            v = v.split(',')
            k = {'sn': sn, 'kpi': v[0], 'label': v[1], 'period': v[2], 'key': v[3], 'axis': v[4]}
        else:
            k = {'sn': None, 'kpi': None, 'label': None, 'period': None, 'key': None, 'axis': None}
        res.append(k)
    return jsonify(res)


# For Robot Detail Page - Chart
@app.route("/chart/data/<sn>/<axis>/<key>/recent/<period>")
def get_chart_data(sn, axis, key, period):
    """
    :param sn: Serial Number
    :param axis: 1 or 6 axis (1 is analog data, 6 is indy axis temperature)
    :param key: count, mean
    :param period: hour
    :return: chart.js dataset
    """

    # print("Opdata Loop SN : %s, Axis : %s, Key : %s, Time : %s" % (sn, axis, key, datetime.now().strftime(fmtAll)))
    if key == 'count':
        sql = "SELECT DATE_FORMAT(CONVERT_TZ(MAX(x), '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') m, " \
              "COUNT(y) from opdatas " \
              "WHERE x >= \"%s\" AND x < \"%s\" AND serial_number = \"%s\" " \
              "GROUP BY ROUND(UNIX_TIMESTAMP(x) / 600) ORDER BY m DESC LIMIT 10" \
              % ((datetime.utcnow() - timedelta(hours=1)).strftime(fmtAll), datetime.utcnow().strftime(fmtAll), sn)
        res = MySQL.select(sql)
        # print("Res : ", res)
        if res is not False and res is not None:
            for i in res:
                i['x'] = i['m']
                i['y'] = i['COUNT(y)']
                del i['m'], i['COUNT(y)']
    elif key == 'mean' and axis == '1':
        sql = "SELECT DATE_FORMAT(CONVERT_TZ(x, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') m, ROUND(AVG(y), 2) " \
              "FROM analog_opdatas " \
              "WHERE x >= \"%s\" AND x < \"%s\" AND serial_number = \"%s\" GROUP BY m ORDER by m DESC LIMIT 80" \
              % ((datetime.utcnow() - timedelta(hours=1)).strftime(fmtAll), datetime.utcnow().strftime(fmtAll), sn)
        res = MySQL.select(sql)
        if res is not False and res is not None:
            for i in res:
                i['x'] = i['m']
                i['y'] = i['ROUND(AVG(y), 2)']
                del i['m'], i['ROUND(AVG(y), 2)']
    elif key == 'mean' and axis == '6':
        sql = "SELECT DATE_FORMAT(CONVERT_TZ(x, '+00:00', '+09:00'), '%%Y-%%m-%%d %%H:%%i:%%S') m, " \
              "AVG(joint0), AVG(joint1), " \
              "AVG(joint2), AVG(joint3), " \
              "AVG(joint4), AVG(joint5) FROM temperature_opdatas " \
              "WHERE x >= \"%s\" AND x < \"%s\" AND serial_number = \"%s\" GROUP BY m ORDER by m DESC LIMIT 80" \
              % ((datetime.utcnow() - timedelta(hours=1)).strftime(fmtAll), datetime.utcnow().strftime(fmtAll), sn)
        res = MySQL.select(sql)
        # print("Temp Res : ", res)

        az = []
        bz = []
        cz = []
        dz = []
        ez = []
        fz = []

        if res is None or type(res) is bool: return jsonify(res)
        for i in res:
            a = {'x': i['m'], 'y': round(i['AVG(joint0)'])}
            b = {'x': i['m'], 'y': round(i['AVG(joint1)'])}
            c = {'x': i['m'], 'y': round(i['AVG(joint2)'])}
            d = {'x': i['m'], 'y': round(i['AVG(joint3)'])}
            e = {'x': i['m'], 'y': round(i['AVG(joint4)'])}
            f = {'x': i['m'], 'y': round(i['AVG(joint5)'])}
            az.append(a)
            bz.append(b)
            cz.append(c)
            dz.append(d)
            ez.append(e)
            fz.append(f)

        aa = [az, bz, cz, dz, ez, fz]
        # print("Temp : ", aa)
        return jsonify(aa)
    else:
        res = None
    # print(res)
    return jsonify(res)

    # todo : Test Code
    # res = [
    #     {'x': (datetime.now() - timedelta(minutes=30)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=60)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=90)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=120)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=150)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=180)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=210)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=240)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=270)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=300)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=330)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=360)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=390)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=420)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=450)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=480)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=510)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=540)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=570)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=600)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=630)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=660)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=690)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=720)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=750)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=780)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=810)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=840)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=870)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=900)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=930)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=960)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=990)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=1200)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=1230)).strftime(fmtAll), 'y': random.randrange(30, 100)},
    #     {'x': (datetime.now() - timedelta(minutes=1260)).strftime(fmtAll), 'y': random.randrange(30, 100)}
    # ]
    #
    # return jsonify(res)


""" Reporter APIs """


@app.route('/ping')
def ping():
    return Response(status=200)


@app.route("/reporter/robot/info", methods=["POST"])
def post_sn_from_reporter():
    if 'sn' not in request.json:
        _sn = ''
    else:
        _sn = request.json['sn']
    if 'company' not in request.json:
        _company = ''
    else:
        _company = request.json['company']
    if 'site' not in request.json:
        _site = ''
    else:
        _site = request.json['site']
    if 'header' not in request.json:
        _header = ''
    else:
        _header = request.json['header']
    if 'model' not in request.json:
        _model = ''
    else:
        _model = request.json['model']

    sql = '''INSERT INTO robots(sn, company, site, header, model) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\") 
    ON DUPLICATE KEY UPDATE site=\"%s\", company=\"%s\", header=\"%s\", model=\"%s\"
    ''' % (_sn, _company, _site, _header, _model, _site, _company, _header, _model)
    if MySQL.insert(sql):
        print("Welcome New S/N Indy")
    else:
        print("Already, S/N Indy")
    return Response('ok')


@app.route("/reporter/robot/state/<sn>", methods=["POST"])
def post_robot_state(sn):
    # todo : State Dic
    _state = json.loads(request.json)
    _ts = datetime.now().timestamp()
    print("Reporter State :", _state)
    cache.hset(sn, 'state', json.dumps(_state))
    if cache.hget(sn, 'ts') is None or _ts - float(cache.hget(sn, 'ts')) > 60 and _state is not None:
        sql = '''INSERT INTO robot_states(serial_number, state) VALUES (\"%s\", \"%s\")
        ''' % (sn, _state)
        MySQL.insert(sql)
        cache.hset(sn, 'ts', _ts)
    return Response("ok")


@app.route("/reporter/robot/event/<sn>", methods=["POST"])
def post_robot_event(sn):
    # todo : Event Down
    # if file is None:
    #     print("No Event File")
    #     return Response('ok')
    #log_save_path = os.path.join(app.config['EVENT_LOG_PATH'])
    # file.save(log_save_path)
    print("Event Log : ", request.json)
    sql = '''INSERT INTO events (json, sn) VALUES (\"%s\", \"%s\")
    ''' % (str(request.json), sn)
    MySQL.insert(sql)
    load_sse_command(sn, '_event')
    return Response('ok')


@app.route("/reporter/robot/clip/<sn>", methods=["POST"])
def post_robot_clip(sn):
    if 'file' in request.files:
        if request.files['file'].name == 'No Camera':
            cache.hset(sn, 'clip', -1)
        else:
            file_name = request.files['file'].filename
            file = request.files['file']
            file.save(os.path.join(app.config['CLIP_UPLOAD_PATH'], file_name))
            time.sleep(0.1)
            cache.hset(sn, 'clip', datetime.now().timestamp())
            time.sleep(0.1)
            cache.hset(sn, 'clip_name', file_name)
        return Response('ok')
    else:
        return Response('ㅗ', status=404)


@app.route("/reporter/chart/data/<sn>", methods=["POST"])
def post_robot_chart_data(sn):
    # todo : Chart Data Dic    if request.method == 'POST':
    # todo : Message Type에 따른 Count, Mean 등 조건으로 나눠서 Query를 변환해야 함
    # mtype, msg, mdata
    print(datetime.now(), request.json)
    if request.json['mtype'] is 1:
        sql = "INSERT INTO opdatas(msg, y, serial_number) " \
              "VALUES (\"%s\", \"%s\", \"%s\") " % (request.json['msg'], request.json['mdata'], sn)
        MySQL.insert(sql)
    elif request.json['mtype'] is 2:
        # print(request.json, len(request.json['mdata']))
        if len(request.json['mdata']) == 1:
            sql = 'INSERT INTO analog_opdatas(msg, serial_number, y) VALUES (\"%s\", \"%s\", \"%s\") ' \
                  % (request.json['msg'], sn, request.json['mdata'])
        else:
            temp = request.json['mdata'].split(',')
            sql = "INSERT INTO temperature_opdatas(msg, serial_number, joint0, joint1, joint2, joint3, joint4, joint5) " \
                  "VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\") " \
                  % (request.json['msg'], sn, temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
                  # % (request.json['msg'], sn, 0, 0, 0, 0, 0, 0)
        MySQL.insert(sql)
    else:
        print("Insert Fail : ", request.json)
    return Response('ok')
    # sql = "INSERT INTO opdatas(x, y) VALUES (\"%s\", \"%s\") " % (request.json['x'], request.json['y'])
    # MySQL.insert(sql)


@app.route("/reporter/robot/kpi/<sn>", methods=["POST"])
def post_robot_kpi(sn):
    # todo : KPI Dic
    # todo : 존재하면 Update로 해야함
    print("Reporter KPI :", request.json)
    if request.json is not None or request.json is not False:
        kpi_num = request.json['mdata'].split(',')[0]
        kpi_str = request.json['mdata']
    else:
        return Response('Fail')
    sql = "INSERT INTO robots (sn, %s) " \
          "VALUES (\"%s\", \"%s\") " \
          "ON DUPLICATE KEY UPDATE %s=\"%s\" " \
          % (kpi_num, sn, kpi_str, kpi_num, kpi_str)
    if MySQL.insert(sql):
        print("Welcome New S/N Indy")
    else:
        print("Already, S/N Indy")
    return Response('ok')


""" Test APIs"""


@app.route("/test", methods=['GET'])
@LoginRequired("user")
def test():
    print(current_user.is_authenticated)
    print(current_user.id)
    return jsonify("Fuck")
