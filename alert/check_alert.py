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
        "msg": f'{title}执行成功'
    }
    else:
    if not error_count:
        alert_bot_msg = {
            "groupId": ALERT_BOT_CODE,
            "msg": f'<div>{title}执行失败，在如下地址查看详情：</div>\n<a href="https://autoui.w.chime.me/#/case">ui自动化测试平台</a>'
        }
    else:
        alert_bot_msg = {
            "groupId": ALERT_BOT_CODE,
            "msg": f'<div>{title}执行失败，对比次数{camp_time}，对比失败次数{error_count}，在如下地址查看详情：</div>\n<a href="https://autoui.w.chime.me/#/case">ui自动化测试平台</a>'
        }


