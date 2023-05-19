import requests
from db_handler.handler_case import *

from env import *


def check_result(model='chrome'):
    cases = query_all_cases_from_tag(model)
    check_count = 0
    error_time = 0
    error_cases = [error_case.title for error_case in cases if error_case.last_succ]
    for case in cases:
        check_count += case.last_comp_count
        error_time += case.last_error_count
    return check_count, error_time, error_cases


def alert_qa():
    url = 'http://alert.d.chime.me/api/notify'
    chrome_check_count, chrome_error_time, chrome_error_cases = check_result('chrome')
    safari_check_count, safari_error_time, safari_error_cases = check_result('safari')

    alert_bot_msg = {
        "groupId": ALERT_BOT_CODE,
        "msg": f'<div>chrome执行情况：共对比次数{chrome_check_count}，失败次数{chrome_error_time}，对比失败案例：{chrome_error_cases}</div>\n'
               f'<div>safari执行情况：共对比次数{safari_check_count}，失败次数{safari_error_time}，对比失败案例：{safari_error_cases}</div>\n'
               f'<a href="https://autoui.w.chime.me/#/case">ui自动化测试平台</a>'
    }

    requests.post(url, json=alert_bot_msg)
