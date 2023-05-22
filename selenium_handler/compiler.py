from db_handler import models


# 变量名称seed
def _init_var_seed():
    global name_var_seed
    name_var_seed = {
        "click": 1,
        "input": 1,
        "text": 1,
        "el": 1,
        "img": 1,
        "el_snapshoot": 1,
        "img_file_path": 1,
        "text_file_path": 1,
        "var_ope": 1,
        "time_log": 1
    }


# 转译字符串
def es_str(s):
    if not s:
        return None
    escape_dict = {'\\': '\\\\', '\"': '\\"', '\'': '\\\'', '\n': '\\n', '\t': '\\t', '\r': '\\r'}
    return s.translate(str.maketrans(escape_dict))


# 获取随机变量名
def _get_random_var_name(type):
    global name_var_seed
    seed = name_var_seed[type]
    name_var_seed[type] += 1
    return f'_{type}_var_{seed}'


# 在最前写入
def _write_chrome_before():
    code = '''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import base64
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--incognito')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(10)
driver.set_window_size(1920, 1280)

    '''
    return code


def _write_safari_before():
    code = '''
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from xvfbwrapper import Xvfb
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import base64
import time
import os

safari_options = Options()
safari_options.add_argument('--incognito')
driver = webdriver.Safari(options=safari_options)
driver.implicitly_wait(10)
driver.set_window_size(1920, 1280)
    '''
    return code


def _write_firefox_before():
    code = """
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import base64
import time
import os

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(10)
driver.set_window_size(1920, 1280)

    """
    return code


# 写在最后
def _write_after():
    code = '''
driver.quit()
    '''
    return code


# 打开页面
def _write_open_page(url):
    code = f'''
driver.get("{url}")
    '''
    return code


# jump
def _write_jump_page(url):
    code = f'''
driver.get("{url}")
        '''
    return code


# 获取selector
def _get_by_selector(type):
    s = "By.XPATH"
    if type == "css":
        s = "By.CSS_SELECTOR"
    elif type == "xpath":
        s = "By.XPATH"
    return s


# 查找元素
def _find_element(var_name, type, val):
    code = f'''
{var_name} = driver.find_element({_get_by_selector(type)}, '{val}')
    '''
    return code


# 点击元素
def _write_click(type, val):
    var_name = _get_random_var_name("click")
    code = f'''
{_find_element(var_name, type, val)}
{var_name}.click()
    '''
    return code


# 输入
def _write_input(type, val, input_val, is_enter=0):
    var_name = _get_random_var_name("input")
    code = f'''
{_find_element(var_name, type, val)}
{var_name}.send_keys("{input_val}"
        '''
    if not is_enter:
        code += ')'
    else:
        code += ', Keys.RETURN)'
    return code


# 输入
def _write_keyword(type=None, val=None, input_val='ENTER'):
    var_name = _get_random_var_name("input")
    code = f'''
{_find_element(var_name, type, val)}
{var_name}.send_keys(Keys.{input_val})
        '''
    return code


# 截图
def _write_snapshot():
    img_name = _get_random_var_name("img") + ".png"
    img_file_path_var = _get_random_var_name("img_file_path")
    code = f'''
{img_file_path_var} = os.path.join(_FIlE_PATH, "{img_name}")
driver.save_screenshot({img_file_path_var})
    '''
    return code, img_file_path_var


# 给某个元素截图
def _write_snapshot_el(type, val):
    el_var_name = _get_random_var_name("el")
    el_snapshoot_var_name = _get_random_var_name("el_snapshoot")
    img_name = _get_random_var_name("img") + ".png"
    img_file_path_var = _get_random_var_name("img_file_path")

    code = f'''
{_find_element(el_var_name, type, val)}
{el_snapshoot_var_name} = {el_var_name}.screenshot_as_png
{img_file_path_var} = os.path.join(_FIlE_PATH, "{img_name}")
with open({img_file_path_var}, 'wb') as f:
    f.write({el_snapshoot_var_name})
    '''
    return code, img_file_path_var


# 等待固定时间
def _write_wait(time_limit):
    code = f'''
time.sleep({time_limit})
    '''
    return code


# 等待某个元素加载完成
def _write_wait_el(type, val, time_limit):
    code = f'''
WebDriverWait(driver, timeout={time_limit}).until(lambda d: d.find_element({_get_by_selector(type)},'{val}'))
    '''
    return code


# 获取文本信息
def _get_text(type, val, var_ope):
    el_var_name = _get_random_var_name("el")
    text_var_name = _get_random_var_name("text") + ".txt"
    text_file_path_var = _get_random_var_name("text_file_path")
    code = f"""
{_find_element(el_var_name, type, val)}
    """
    if var_ope.get('option') in ['compare', 'showInResult']:
        code += f'''
{text_file_path_var} = os.path.join(_FIlE_PATH, "{text_var_name}")
with open({text_file_path_var}, "w") as f:
    f.write({el_var_name}.text)
        '''
    elif var_ope.get('option') == 'compText':
        code = f'''
if {var_ope.get('Text')} != {el_var_name}.text:
    raise ValueError('预期文案:{var_ope.get('Text')}，实际文案:{el_var_name}.text')
        '''

    return code, text_file_path_var


# 处理code格式
def _handle_code_(code):
    return "\n".join(filter(lambda item: item.strip() != "", code.split("\n")))


# 编写变量操作
def _write_var_operation(var_name, ope, ope_name, ope_type):
    var_var_name = _get_random_var_name("var_ope")
    code = f'''
{var_var_name} = {{
    "varOpeType": "{ope}",
    "varOpeValue": {var_name},
    "opeName": "{ope_name}",
    "opeType": "{ope_type}"
}}
_VAR_OPE_RECORD_.append({var_var_name})
    '''
    return code


# 编写错误捕获
def _write_try_catch(code, ope_type, ope_name):
    code = "    " + code.replace("\n", "\n    ")
    time_log_name = _get_random_var_name("time_log")
    code = f'''
try :
    {time_log_name} = {{
        "opeType": "{ope_type}",
        "opeName": "{ope_name}",
        "type": "start"
    }}
    _TIME_LOGGER_({time_log_name})
{code}
    {time_log_name}["type"] = "end"
    _TIME_LOGGER_({time_log_name})
except Exception as e:
    _ERROR_LOGGER_(e, {{
        "opeType": "{ope_type}",
        "opeName": "{ope_name}",
        "ignoreError": {ope_type == "try-to-click"}
    }})
    '''
    return code


def _write_code(operations):
    tmp = ''
    for operation in operations:
        ope_type = operation.get("opeType")
        ope_name = operation.get("opeName")
        ov = operation.get("value")
        ef = ov.get("elFinder")
        var_ope = ov.get("varOpe")

        operation_code = ""
        var_name = ""
        if ope_type == "open-page":
            operation_code = _write_open_page(es_str(ov["url"]))
        elif ope_type == "jump":
            operation_code = _write_jump_page(es_str(ov["url"]))
        elif ope_type == "click":
            operation_code = _write_click(ef["findType"], es_str(ef["findVal"]))
        elif ope_type == "try-to-click":
            operation_code = _write_click(ef["findType"], es_str(ef["findVal"]))
        elif ope_type == "input":
            operation_code = _write_input(ef["findType"], es_str(ef["findVal"]), es_str(ov["inputVal"]),
                                          ov.get("isEnter"))
        elif ope_type == "keyword-opt":
            operation_code = _write_keyword(ef["findType"], es_str(ef["findVal"]), es_str(ov.get('keywordOpt')))
        elif ope_type == "wait":
            operation_code = _write_wait(ov["timeLimit"])
        elif ope_type == "wait-el":
            operation_code = _write_wait_el(ef["findType"], es_str(ef["findVal"]), ov["timeLimit"])
        elif ope_type == "snapshot":
            operation_code, var_name = _write_snapshot()
        elif ope_type == "snapshot-el":
            operation_code, var_name = _write_snapshot_el(ef["findType"], es_str(ef["findVal"]))
        elif ope_type == "get-text":
            operation_code, var_name = _get_text(ef["findType"], es_str(ef["findVal"]), var_ope)
        elif ope_type == "other-process":
            other_process_id = ov.get('otherProcessId')
            db_operations = models.Operation.objects.filter(process_id=other_process_id)
            opts = []
            for db_operation in db_operations:
                json_operation = db_operation.to_dict()
                opts.append(json_operation)
            tmp += _write_code(opts)
        if var_name != "":
            operation_code += _write_var_operation(var_name, var_ope.get("option"), ope_name, ope_type)
        if operation_code:
            operation_code = _handle_code_(operation_code)
            operation_code = _write_try_catch(operation_code, ope_type, ope_name)
            tmp += operation_code
    return tmp


def compile_code(operations, model='chrome'):
    _init_var_seed()
    if model == 'firefox':
        code = _write_firefox_before()
    elif model == 'safari':
        code = _write_safari_before()
    else:
        code = _write_chrome_before()
    code += _write_code(operations)
    code += _write_after()
    return code
