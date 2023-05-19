import os
import shutil

from django.conf import settings

BASE_DIR = settings.BASE_DIR


def add_file(case_id):
    case_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}")
    os.makedirs(case_file_path)


def del_file(case_id):
    case_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}")
    if os.path.isdir(case_file_path):
        shutil.rmtree(case_file_path)


def del_norm_file(case_id):
    norm_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}", 'norm')
    shutil.rmtree(norm_file_path)


def del_current_file(case_id):
    cur_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}", 'current')
    shutil.rmtree(cur_file_path)


def mv_current_to_norm(case_id):
    norm_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}", 'norm')
    cur_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}", 'current')
    shutil.move(cur_file_path, norm_file_path)
