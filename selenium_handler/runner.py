import logging
import os
from datetime import datetime
import time
from django.conf import settings
import cv2
import numpy as np
import tensorflow as tf
from env import *
import html
import psutil

BASE_DIR = settings.BASE_DIR
logger = logging.getLogger(__name__)


class RunCodeException(Exception):
    msg = ""

    def __int__(self, msg):
        self.msg = msg


def get_curr_time_str():
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return f'Time : {date_time_str}'


def get_var_info(ope_name, url, model='chrome'):
    if ope_name == "get-text":
        url = os.path.join(BASE_DIR, "../", url)
        with open(url, "r") as f:
            content = f.read()
            content = f'''
            <span title="{ope_name}" class="el-text">{content}</span>
            '''
    else:
        content = f'''
        <img title="{ope_name}" class="snap-img" src="/api/case/getPic?fileUrl={url}&model={model}" />
        '''
    return content


def load_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.resnet50.preprocess_input(img)
    return img


def image_similarity(image_path1, image_path2):
    model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, pooling='avg')
    img1 = load_image(image_path1)
    img2 = load_image(image_path2)
    feature1 = model.predict(img1)
    feature2 = model.predict(img2)
    similarity = np.dot(feature1, feature2.T) / (np.linalg.norm(feature1) * np.linalg.norm(feature2))
    return similarity


def compare_vars(ope_name, url1, url2):
    url1 = os.path.join('/', url1)
    url2 = os.path.join('/', url2)
    if ope_name == "get-text":
        with open(url1, "r") as f:
            content1 = f.read()
        with open(url2, "r") as f:
            content2 = f.read()
        return ("Equal", 0) if content1 == content2 else ("Not Equal", 1)
    else:
        similarity = round(image_similarity(url1, url2)[0][0], 4) * 100
        return (f'{similarity}%', 0) if similarity > LOWEST_SIMILARITY else (f'{similarity}%', 1)


def format_str(content):
    return html.escape(content)


def run_case(code, options, model='chrome'):
    # code内使用的文件夹根路径
    cfp = options.get("caseFilePath")
    run_norm = options.get("runNorm")
    _FIlE_PATH = os.path.join(cfp, "norm" if run_norm else "current")

    # 根目录不存在，创建根目录
    if not os.path.exists(_FIlE_PATH):
        os.makedirs(_FIlE_PATH)

    # 日志
    logs = [
        f'{get_curr_time_str()} Start run: norm({run_norm})'
    ]

    def append_log(log_type, content):
        logs.append(f'''
        <div class="run-log {log_type}">
            {content}
        </div>
        ''')

    # code内时间日志
    def _TIME_LOGGER_(options):
        if options["type"] == "start":
            append_log(
                "start",
                f'{get_curr_time_str()} Run "{options["opeName"]}" {options["type"]}.'
            )
        else:
            append_log("end", "end")

    # code内使用的错误日志函数
    def _ERROR_LOGGER_(e, options):
        if options.get("ignoreError"):
            append_log(
                "ignore-error",
                f'{get_curr_time_str()} Run "{options["opeName"]}" failed, but we\'ve ignore this exception。'
            )
        else:
            append_log(
                "error",
                f'{get_curr_time_str()} Run "{options["opeName"]}" failed with reason:{repr(e)}'
            )
            raise e

    has_error = False
    # 变量操作容器
    _VAR_OPE_RECORD_ = []
    for i in range(RETRY):
        try:
            # 变量操作容器
            _VAR_OPE_RECORD_ = []
            # run code
            exec(code)
            break
        except Exception as e:
            logging.error(options['caseId'])
            logging.error(e)
            append_log(
                "ignore-error",
                f"retry {i + 1} end"
            )
            time.sleep(5)
    else:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'safari':
                proc.kill()

        has_error = True
        append_log(
            "error",
            "Execution failed after 3 attempts"
        )

    error_count = 0

    append_log("complete", 'Complete!')
    camp_time = 0
    if len(_VAR_OPE_RECORD_):
        append_log("tip", 'Variable operation result:')
        for r in _VAR_OPE_RECORD_:
            var_ope_type = r.get("varOpeType")
            var_ope_val = os.path.normpath(r.get("varOpeValue"))
            var_ope_name = r.get("opeName")
            ope_type = r.get("opeType")

            if var_ope_type == "showInResult" or run_norm:
                url = os.path.join(*(var_ope_val.split(os.sep)[-4:]))
                append_log("ope-item", f'''
                <div class="ope-info">Operation '{var_ope_name}' result:</div>
                <div class="result">
                    {get_var_info(ope_type, url, model)}
                </div>
                ''')
            else:
                camp_time += 1
                sp_path = var_ope_val.split(os.sep)
                sp_path[-2] = "norm"
                norm_ope_val = os.path.join(*sp_path)
                norm_url = os.path.join(*(str(norm_ope_val).split(os.sep)[-4:]))
                curr_url = os.path.join(*(var_ope_val.split(os.sep)[-4:]))
                compare_result, compare_status = compare_vars(ope_type, norm_ope_val, var_ope_val)
                append_log("ope-item", f'''
                <div class="ope-info">Operation '{var_ope_name}' result:</div>
                    <div class="result">
                        <div class="norm">{get_var_info(ope_type, norm_url, model)}</div>
                        <div class="current">{get_var_info(ope_type, curr_url, model)}</div>
                    </div>
                    <div class="compare-result-">
                        <div>Compare Result:</div>
                        <div class="ans">{compare_result}</div>
                    </div>
                ''')

                if compare_status:
                    error_count += 1
    else:
        append_log("tip", 'No variable operation.')

    return has_error, "\n".join(logs), error_count, camp_time
