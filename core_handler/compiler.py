from db_handler.handler_operation import *


class CompileCode:
    text = 1
    img = 1
    img_file_path = 1
    text_file_path = 1
    code = ""
    tmp = ""

    @staticmethod
    def _es_str(s):
        if not s:
            return None
        escape_dict = {'\\': '\\\\', '\"': '\\"', '\'': '\\\'', '\n': '\\n', '\t': '\\t', '\r': '\\r'}
        return s.translate(str.maketrans(escape_dict))

    @staticmethod
    def _handle_code_(code, ope_type, ope_name, ignore=False):
        code = "\n".join(filter(lambda item: item.strip() != "", code.split("\n")))
        code = "    " + code.replace("\n", "\n    ")
        code = f'''
    try :
        self._time_log_var = {{
            "opeType": "{ope_type}",
            "opeName": "{ope_name}",
            "type": "start",
            "ignoreError": {ignore}
        }}
        self._time_logger(self._time_log_var)
{code}
        self._time_log_var["type"] = "end"
        self._time_logger(self._time_log_var)
    except Exception as e:
        self._error_logger(e, self._time_log_var)
'''
        return code

    def _write_before(self, model='chrome'):
        before_dic = {
            'chrome': '''
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    self.browser = playwright.chromium.launch(headless=True)
    self.context = self.browser.new_context()
    self.page = self.context.new_page()
    self.page.set_viewport_size({"width": 1920, "height": 1280})
''',
            'safari': '''
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    self.browser = playwright.webkit.launch(headless=True)
    self.context = self.browser.new_context()
    self.page = self.context.new_page()
    self.page.set_viewport_size({"width": 1920, "height": 1280})
''',
            'firefox': '''
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    self.browser = playwright.firefox.launch(headless=True)
    self.context = self.browser.new_context()
    self.page = self.context.new_page()
    self.page.set_viewport_size({"width": 1920, "height": 1280})
'''
        }
        self.code += before_dic[model]

    def _write_open_page(self, url, ope_type, ope_name):
        self.tmp = f'''
    self.page.goto("{url}")
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_jump_page(self, find_val, ope_type, ope_name):
        self.tmp = f'''
    with self.context.expect_page() as new_page_info:
        self.page.click('{find_val}')
    self.old_page = self.page
    self.page = new_page_info.value
    self.page.wait_for_load_state()

'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_click(self, find_val, ope_type, ope_name, ignore=True):
        self.tmp = f'''
    self.page.click('{find_val}')
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name, ignore)

    def _write_input(self, find_val, input_val, ope_type, ope_name, is_enter=0):
        self.tmp = f'''
    self.page.fill('{find_val}', '{input_val}')
'''
        if is_enter:
            self.tmp += '''
    time.sleep(2)
    self.page.keyboard.press("Enter")
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_keyword(self, ope_type, ope_name, find_val='', input_val='Enter'):
        if find_val:
            self.tmp = f'''
    self.page.locator("{find_val}").press("{input_val}")
'''
        else:
            self.tmp = f'''
    self.page.keyboard.press("{input_val}")
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_wait(self, time_limit, ope_type, ope_name):
        self.tmp = f'''
    time.sleep({time_limit})
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_wait_el(self, find_val, ope_type, ope_name):
        self.tmp = f'''
    self.page.wait_for_selector('{find_val}')
'''
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_snapshot(self, ope_type, ope_name, var_ope, find_val=''):
        img_name = f"_img_var_{self.img}" + ".png"
        self.img += 1
        img_file_path_var = f"_img_file_path_var_{self.img_file_path}"
        self.img_file_path += 1
        if find_val:
            self.tmp = f'''
    {img_file_path_var} = os.path.join(self._FILE_PATH, "{img_name}")
    self.page.locator("{find_val}").screenshot(path={img_file_path_var})
'''
        else:
            self.tmp = f'''
    {img_file_path_var} = os.path.join(self._FILE_PATH, "{img_name}")
    self.page.screenshot(path={img_file_path_var})
'''
        self._write_var_operation(img_file_path_var, var_ope, ope_name, ope_type)
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _get_text(self, find_val, var_ope, ope_type, ope_name):
        text_var_name = f"_text_var_{self.text}" + ".txt"
        self.text += 1
        text_file_path_var = f"_text_file_path_var_{self.text_file_path}"
        self.text_file_path += 1

        if var_ope.get('option') in ['compare', 'showInResult']:
            self.tmp = f'''
    text = self.page.locator('{find_val}').text_content()
    {text_file_path_var} = os.path.join(self._FILE_PATH, "{text_var_name}")
    with open({text_file_path_var}, "w") as f:
        f.write(text)
'''
        elif var_ope.get('option') == 'compText':
            self.tmp = f'''
    text = self.page.locator('{find_val}').text_content()
    if {var_ope.get('Text')} != text:
        raise ValueError('预期结果: {var_ope.get('Text')}，实际结果: ' + text)
'''
        self._write_var_operation(text_file_path_var, var_ope.get("option"), ope_name, ope_type)
        self.code += self._handle_code_(self.tmp, ope_type, ope_name)

    def _write_var_operation(self, var_name, var_ope, ope_name, ope_type):
        self.tmp += f'''
    self._VAR_OPE_RECORD_.append({{
        "varOpeType": "{var_ope}",
        "varOpeValue": {var_name},
        "opeName": "{ope_name}",
        "opeType": "{ope_type}"
    }})
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
                self._write_jump_page(self._es_str(ef["url"]), ope_type, ope_name)
            elif ope_type == "click":
                self._write_click(self._es_str(ef["findVal"]), ope_type, ope_name)
            elif ope_type == "try-to-click":
                self._write_click(self._es_str(ef["findVal"]), ope_type, ope_name, True)
            elif ope_type == "input":
                self._write_input(self._es_str(ef["findVal"]), self._es_str(ov["inputVal"]), ope_type, ope_name,
                                  ov.get("isEnter"))
            elif ope_type == "keyword-opt":
                self._write_keyword(ope_type, ope_name, self._es_str(ef["findVal"]), self._es_str(ov.get('keywordOpt')))
            elif ope_type == "wait":
                self._write_wait(ov["timeLimit"], ope_type, ope_name)
            elif ope_type == "wait-el":
                self._write_wait_el(self._es_str(ef["findVal"]), ope_type, ope_name)
            elif ope_type == "snapshot":
                self._write_snapshot(ope_type, ope_name, var_ope.get("option"))
            elif ope_type == "snapshot-el":
                self._write_snapshot(ope_type, ope_name, var_ope.get("option"), self._es_str(ef["findVal"]))
            elif ope_type == "get-text":
                self._get_text(self._es_str(ef["findVal"]), var_ope, ope_type, ope_name)
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
    self.context.close()
    self.browser.close()

        '''

    def compile_code(self, operations, model='chrome'):
        self._write_before(model)
        self._write_code(operations)
        self._write_after()
        return self.code
