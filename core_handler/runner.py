import logging
import os
import time
from datetime import datetime
from django.conf import settings
import cv2
import numpy as np
import tensorflow as tf
from env import *
import html

BASE_DIR = settings.BASE_DIR
MEDIA_ROOT = settings.MEDIA_ROOT
logger = logging.getLogger(__name__)


def get_curr_time_str():
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return f'Time : {date_time_str}'


def get_var_info(ope_name, url, model='chrome'):
    if ope_name == "get-text":
        url = os.path.join(MEDIA_ROOT, url)
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


class Run:
    def __init__(self, options):
        self.page = None
        self.context = None
        self.browser = None
        self.old_page = None
        self.options = options
        self.run_norm = self.options.get("runNorm")
        self._FILE_PATH = os.path.join(options.get("caseFilePath"), "norm" if self.run_norm else "current")
        os.makedirs(self._FILE_PATH, exist_ok=True)
        self.logs = [
            f'{get_curr_time_str()} Start run: norm({self.run_norm})'
        ]
        self.has_error = False
        self._VAR_OPE_RECORD_ = []
        self._time_log_var = {}

    def append_log(self, log_type, content):
        self.logs.append(f'''
        <div class="run-log {log_type}">
            {content}
        </div>
        ''')

    def _time_logger(self, opt):
        if opt["type"] == "start":
            self.append_log(
                "start",
                f'{get_curr_time_str()} Run "{opt["opeName"]}" {opt["type"]}.'
            )
        else:
            self.append_log("end", "end")

    def _error_logger(self, exc, opt):
        if opt.get("ignoreError"):
            self.append_log(
                "ignore-error",
                f'{get_curr_time_str()} Run "{opt["opeName"]}" failed, but we\'ve ignore this exception。'
            )
        else:
            self.append_log(
                "error",
                f'{get_curr_time_str()} Run "{opt["opeName"]}" failed with reason:{repr(exc)}'
            )
            self.context.close()
            self.browser.close()
            logging.error(exc)
            raise exc

    def run_case(self, code, model='chrome'):
        for i in range(RETRY):
            try:
                self._VAR_OPE_RECORD_ = []
                exec(code)
                break
            except Exception as exc:
                logging.error('---------------------------------------')
                logging.error(self.options['caseId'])
                logging.error(exc)
                logging.error('---------------------------------------')
                self.append_log(
                    "ignore-error",
                    f"retry {i + 1} end"
                )
                time.sleep(5)
        else:
            self.has_error = True
            self.append_log(
                "error",
                "Execution failed after 3 attempts"
            )

        error_count = 0

        self.append_log("complete", 'Complete!')
        camp_time = 0
        if len(self._VAR_OPE_RECORD_):
            self.append_log("tip", 'Variable operation result:')
            for r in self._VAR_OPE_RECORD_:
                var_ope_type = r.get("varOpeType")
                var_ope_val = os.path.normpath(r.get("varOpeValue"))
                var_ope_name = r.get("opeName")
                ope_type = r.get("opeType")

                if var_ope_type == "showInResult" or self.run_norm:
                    url = os.path.join(*(var_ope_val.split(os.sep)[-4:]))
                    self.append_log("ope-item", f'''
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
                    self.append_log("ope-item", f'''
                    <div class="ope-info">Operation '{var_ope_name}' result:</div>
                        <div class="result">
                            <div class="norm">{get_var_info(ope_type, norm_url, model)}</div>
                            <div class="current">{get_var_info(ope_type, curr_url, model)}</div>
                        </div>
                        <div class="compare-result-">
                            <div>Compare Result:</div>
                            <div class="ans" error_tag={compare_status}>{compare_result}</div>
                        </div>
                    ''')

                    if compare_status:
                        error_count += 1
        else:
            self.append_log("tip", 'No variable operation.')

        return self.has_error, "\n".join(self.logs), error_count, camp_time
