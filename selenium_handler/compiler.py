from db_handler.handler_operation import *


class CompileCode:
    click = 1
    input = 1
    text = 1
    el = 1
    img = 1
    el_snapshot = 1
    img_file_path = 1
    text_file_path = 1
    var_ope = 1
    code = ""
    tmp = ""

    @staticmethod
    def _es_str(s):
        if not s:
            return None
        escape_dict = {'\\': '\\\\', '\"': '\\"', '\'': '\\\'', '\n': '\\n', '\t': '\\t', '\r': '\\r'}
        return s.translate(str.maketrans(escape_dict))

    @staticmethod
    def _handle_code_(code, ope_type, ope_name):
        code = "\n".join(filter(lambda item: item.strip() != "", code.split("\n")))
        code = "    " + code.replace("\n", "\n    ")
        code = f'''
try :
    self._time_log_var = {{
        "opeType": "{ope_type}",
        "opeName": "{ope_name}",
        "type": "start",
        "ignoreError": {ope_type == "try-to-click"}
    }}
    self._time_logger(self._time_log_var)
{code}
    self._time_log_var["type"] = "end"
    self._time_logger(self._time_log_var)
except Exception as e:
    self._error_logger(driver, e, self._time_log_var)
        '''
        return code

    @staticmethod
    def _get_by_selector(select_type):
        return "By.CSS_SELECTOR" if select_type == 'css' else "By.XPATH"

    def _write_before(self, model='chrome'):
        before_dic = {
            'chrome': '''
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
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
driver.set_window_size(1920, 1280)

''',
            'safari': '''
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

''',
            'firefox': '''
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

'''
        }
        self.code += before_dic[model]

    def _write_open_page(self, url, ope_type, ope_name):
        self.tmp = f'''
driver.get("{url}")
        '''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_jump_page(self, ope_type, ope_name):
        self.tmp = f'''
current_handle = driver.current_window_handle
all_handles = driver.window_handles
new_handle = None
for handle in all_handles:
    if handle != current_handle:
        new_handle = handle
        break
driver.switch_to.window(new_handle)
driver.set_window_size(1920, 1280)

            '''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_click(self, find_type, find_val, ope_type, ope_name):
        var_name = f"_click_var_{self.click}"
        self.click += 1
        self.tmp = f'''
{var_name} = driver.find_element({self._get_by_selector(find_type)}, '{find_val}')
{var_name}.click()
        '''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_input(self, find_type, find_val, input_val, ope_type, ope_name, is_enter=0):
        var_name = f"_input_var_{self.input}"
        self.input += 1
        self.tmp = f'''
{var_name} = driver.find_element({self._get_by_selector(find_type)}, '{find_val}')
{var_name}.send_keys("{input_val}" {", Keys.RETURN)" if is_enter else ")"}
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_keyword(self, find_type, find_val, ope_type, ope_name, input_val='ENTER'):
        var_name = f"_input_var_{self.input}"
        self.input += 1
        self.tmp = f'''
{var_name} = driver.find_element({self._get_by_selector(find_type)}, '{find_val}')
{var_name}.send_keys(Keys.{input_val})
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_wait(self, time_limit, ope_type, ope_name):
        self.tmp = f'''
time.sleep({time_limit})
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_wait_el(self, find_type, find_val, time_limit, ope_type, ope_name):
        self.tmp = f'''
WebDriverWait(driver, timeout={time_limit}).until(lambda d: d.find_element({self._get_by_selector(find_type)}, '{find_val}'))
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_snapshot(self, ope_type, ope_name, var_ope):
        img_name = f"_img_var_{self.img}" + ".png"
        self.img += 1
        img_file_path_var = f"_img_file_path_var_{self.img_file_path}"
        self.img_file_path += 1
        self.tmp = f'''
{img_file_path_var} = os.path.join(self._FILE_PATH, "{img_name}")
driver.save_screenshot({img_file_path_var})
'''
        self._write_var_operation(img_file_path_var, var_ope, ope_name, ope_type)
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)
        return img_file_path_var

    def _write_snapshot_el(self, find_type, find_val, ope_type, ope_name, var_ope):
        el_var_name = f"_el_var_{self.el}"
        self.el += 1
        el_snapshot_var_name = f"_el_snapshot_var_{self.el_snapshot}"
        self.el_snapshot += 1
        img_name = f"_img_var_{self.img}" + ".png"
        self.img += 1
        img_file_path_var = f"_img_file_path_var_{self.img_file_path}"
        self.img_file_path += 1

        self.tmp = f'''
{el_var_name} = driver.find_element({self._get_by_selector(find_type)}, '{find_val}')
{el_snapshot_var_name} = {el_var_name}.screenshot_as_png
{img_file_path_var} = os.path.join(self._FILE_PATH, "{img_name}")
with open({img_file_path_var}, 'wb') as f:
    f.write({el_snapshot_var_name})
'''
        self._write_var_operation(img_file_path_var, var_ope, ope_name, ope_type)
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)
        return img_file_path_var

    def _get_text(self, find_type, find_val, var_ope, ope_type, ope_name):
        el_var_name = f"_el_var_{self.el}"
        self.el += 1
        text_var_name = f"_text_var_{self.text}" + ".txt"
        self.text += 1
        text_file_path_var = f"_text_file_path_var_{self.text_file_path}"
        self.text_file_path += 1

        self.tmp = f"""
{el_var_name} = driver.find_element({self._get_by_selector(find_type)}, '{find_val}')
        """
        if var_ope.get('option') in ['compare', 'showInResult']:
            self.tmp += f"""
{text_file_path_var} = os.path.join(self._FILE_PATH, "{text_var_name}")
with open({text_file_path_var}, "w") as f:
    f.write({el_var_name}.text)
"""
        elif var_ope.get('option') == 'compText':
            self.tmp = f"""
if {var_ope.get('Text')} != {el_var_name}.text:
    raise ValueError('预期文案:{var_ope.get('Text')}，实际文案:{el_var_name}.text')
"""
        self._write_var_operation(text_file_path_var, var_ope.get("option"), ope_name, ope_type)
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)
        return text_file_path_var

    def _write_var_operation(self, var_name, var_ope, ope_name, ope_type):
        var_var_name = f"_var_ope_var_{self.var_ope}"
        self.var_ope += 1
        self.tmp += f'''
{var_var_name} = {{
    "varOpeType": "{var_ope}",
    "varOpeValue": {var_name},
    "opeName": "{ope_name}",
    "opeType": "{ope_type}"
}}
self._VAR_OPE_RECORD_.append({var_var_name})
'''

    def _write_code(self, operations):
        for operation in operations:
            ope_type = operation.get("opeType")
            ope_name = operation.get("opeName")
            ov = operation.get("value")
            ef = ov.get("elFinder")
            var_ope = ov.get("varOpe")

            if ope_type == "open-page":
                self._write_open_page(self._es_str(ov["url"]), ope_type, ope_name)
            elif ope_type == "jump":
                self._write_jump_page(ope_type, ope_name)
            elif ope_type in ["click", "try-to-click"]:
                self._write_click(ef["findType"], self._es_str(ef["findVal"]), ope_type, ope_name)
            elif ope_type == "input":
                self._write_input(ef["findType"], self._es_str(ef["findVal"]), self._es_str(ov["inputVal"]), ope_type,
                                  ope_name,
                                  ov.get("isEnter"))
            elif ope_type == "keyword-opt":
                self._write_keyword(ef["findType"], self._es_str(ef["findVal"]), self._es_str(ov.get('keywordOpt')),
                                    ope_type,
                                    ope_name)
            elif ope_type == "wait":
                self._write_wait(ov["timeLimit"], ope_type, ope_name)
            elif ope_type == "wait-el":
                self._write_wait_el(ef["findType"], self._es_str(ef["findVal"]), ov["timeLimit"], ope_type, ope_name)
            elif ope_type == "snapshot":
                self._write_snapshot(ope_type, ope_name, var_ope.get("option"))
            elif ope_type == "snapshot-el":
                self._write_snapshot_el(ef["findType"], self._es_str(ef["findVal"]), ope_type, ope_name,
                                        var_ope.get("option"))
            elif ope_type == "get-text":
                self._get_text(ef["findType"], self._es_str(ef["findVal"]), var_ope, ope_type, ope_name)
            elif ope_type == "other-process":
                other_process_id = ov.get('otherProcessId')
                db_operations = query_operations(process_id=other_process_id)
                opts = []
                for db_operation in db_operations:
                    json_operation = db_operation.to_dict()
                    opts.append(json_operation)
                self._write_code(opts)

    def _write_after(self):
        self.code += '''
driver.quit()
        '''

    def compile_code(self, operations, model='chrome'):
        self._write_before(model)
        self._write_code(operations)
        self._write_after()
        return self.code
