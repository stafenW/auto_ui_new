import os
import shutil

from django.conf import settings
from db_handler.handler_process_relation_img import query_img_path, query_thumbnail_path

BASE_DIR = settings.BASE_DIR
MEDIA_ROOT = settings.MEDIA_ROOT


def add_snapshot_direct(case_id):
    case_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}")
    os.makedirs(case_file_path)


def del_snapshot_direct(case_id):
    case_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}")
    if os.path.isdir(case_file_path):
        shutil.rmtree(case_file_path)


def del_norm_direct(case_id):
    norm_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}", 'norm')
    shutil.rmtree(norm_file_path)


def del_current_direct(case_id):
    cur_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}", 'current')
    shutil.rmtree(cur_file_path)


def snapshot_file_mv_current_to_norm(case_id):
    norm_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}", 'norm')
    cur_file_path = os.path.join(BASE_DIR, "case-records", f"case-{case_id}", 'current')
    shutil.rmtree(norm_file_path)
    os.rename(cur_file_path, norm_file_path)


def add_process_description_img_direct(process_id):
    process_file_path = os.path.join(BASE_DIR, "description", f"process-{process_id}")
    os.makedirs(process_file_path)


def delete_process_description_img_direct(process_id):
    process_file_path = os.path.join(BASE_DIR, "media", "process_images", str(process_id))
    if os.path.isdir(process_file_path):
        shutil.rmtree(process_file_path)


def get_process_description_img_path(process_id):
    return os.path.join(MEDIA_ROOT, query_img_path(process_id=process_id))


def get_process_description_thumbnail_path(process_id):
    return os.path.join(MEDIA_ROOT, query_thumbnail_path(process_id=process_id))
