import json, os

CONFIG_PATH = os.path.join('/home/user/release/IndyCAREReporter', 'reporter_conf/')
# print(CONFIG_PATH)
try:
    with open(CONFIG_PATH + 'indyCAREConfig.json') as file:
        json_data = json.load(file)
        # print(data)

    URL = json_data['url']
    COMPANY = json_data['company']
    SITE = json_data['site']
    HEADER = json_data['header']
    MODEL = json_data['model']
except Exception as e:
    print("Config.py Error! Please Check the indyCAREConfig.json : ",  e)
    raise e
