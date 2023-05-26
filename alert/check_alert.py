import requests
from db_handler.handler_case import *

from env import *


def check_result(model='chrome'):
    cases = query_all_cases_from_tag(model)
    check_count = 0
    error_time = 0
    error_cases = [error_case.title for error_case in cases if error_case.last_succ == 2]
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
        "msg": f'<div style="font-size: larger; font-weight: bold;">chrome execute result: </div>\n'
               f'<div>compare time {chrome_check_count}, error time {chrome_error_time}, '
               f'error case {chrome_error_cases}</div>\n'
               f'<div style="font-size: larger; font-weight: bold;">safari execute result: </div>\n'
               f'<div>compare time {safari_check_count}, error time {safari_error_time}, '
               f'error case {safari_error_cases}</div>\n'
               f'<a href="{PLATFORM_URL}">Click here to enter the UI automation testing platform</a>'
    }

    response = requests.post(url, json=alert_bot_msg)
    return response
