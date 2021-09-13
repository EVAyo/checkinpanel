import os

import json5 as json

import env_utils

# 缓存全局的环境
DATA = {}


def get_data() -> object:
    """
    获取签到的配置文件。

    :return: 签到配置文件对象
    """
    global DATA
    if DATA: return DATA

    if check_config := os.getenv('CHECK_CONFIG'):
        if not os.path.exists(check_config):
            print(f'错误：环境变量 CHECK_CONFIG 指定的配置文件 {check_config} 不存在！')
            exit(1)
    else:
        check_config = env_utils.get_file_path('check.json') or env_utils.get_file_path('check.json5')
        if not check_config:
            print('错误：未检查到签到配置文件，请在指定位置创建文件或设置 CHECK_CONFIG 指定你的文件。')
            exit(1)

    try:
        DATA = json.load(open(check_config, "r", encoding="utf-8"))
        return DATA
    except ValueError:
        print(f'错误：配置文件 {check_config} 格式不对，请在 https://verytoolz.com/json5-validator.html 中检查格式')
