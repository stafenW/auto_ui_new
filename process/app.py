import os.path
import time

from django.http import HttpResponse

from db_handler.handler_process import *
from db_handler.handler_process_tag import *
from db_handler.handler_process_relate_tag import *
from db_handler.handler_process_relation_img import *
from file_handler.handler_file import *
import json

MEDIA_ROOT = settings.MEDIA_ROOT


def app_add_process_and_operation(process, image_data):
    title = process.get("title")
    describe = process.get("describe")
    ope_list = process.get("operations")
    tag_list = process.get("tagIds")

    now = datetime.now()
    new_process_id = add_process_ope(title, describe, now.strftime("%Y-%m-%d %H:%M:%S"))
    if ope_list:
        ope_list = json.loads(ope_list)
        add_operations(ope_list, new_process_id)
    if tag_list:
        add_relates(json.loads(tag_list), new_process_id)
    if image_data:
        add_process_description_img(new_process_id, image_data)

    return query_process(new_process_id).to_dict()


def app_delete_process_and_ope(process_id):
    delete_process_description_img_direct(process_id)
    return del_process_ope(process_id)


def app_update_process_and_operation_and_relation(process, image_data):
    process_id = process.get("id")
    process_title = process.get("title")
    process_description = process.get("describe")
    process_operation_list = process.get("operations")
    process_tag_list = process.get("tagIds")

    update_process_descript(process_id, title=process_title, describe=process_description)
    update_operations(process_operation_list, process_id)
    if process_tag_list:
        update_relation(process_id, process_tag_list)
    if image_data:
        delete_process_description_img_direct(process_id)
        update_process_description_img(process_id, image_data)
    return query_process(process_id).to_dict()


def app_update_process_tag_relation(process_id, tag_ids):
    update_relation(process_id, tag_ids)
    return True


def app_process_list(title='', tag_ids=None):
    if title and tag_ids:
        process_id_list = query_process_id_list_from_tag(tag_ids)
        process_list = query_process_from_filter(title__icontains=title, id__in=process_id_list)
    elif title and not tag_ids:
        process_list = query_process_from_filter(title__icontains=title)
    elif not title and tag_ids:
        process_id_list = query_process_id_list_from_tag(tag_ids)
        process_list = query_process_from_filter(id__in=process_id_list)
    else:
        process_list = query_process_from_filter()

    process_dicts = []

    process_ids = [process.id for process in process_list]
    pic_path_dict = query_pic_paths_to_dict(process_ids)
    operations_count_dict = query_operations_count_to_dict(process_ids)
    tags_dict = query_tags_of_processes_to_dict(process_ids)

    for process in process_list:
        process_dict = process.to_dict()
        img_path, thumbnail_path = pic_path_dict.get(process.id, (False, False))

        if img_path:
            process_dict["thumbnailUrl"] = thumbnail_path
            process_dict["imageUrl"] = img_path
        process_dict["tag"] = tags_dict.get(process.id, [])
        process_dict["step"] = operations_count_dict.get(process.id, 0)
        process_dicts.append(process_dict)
    return process_dicts


def app_process_detail(process_id):
    process = query_process(process_id)
    process_dict = process.to_dict()
    process_dict["operations"] = [ope.to_dict() for ope in query_operations(process_id)]
    img_path, thumbnail_path = query_pic_path(process.id)
    if img_path:
        process_dict["thumbnailUrl"] = thumbnail_path
        process_dict["imageUrl"] = img_path
    process_dict["tag"] = [tag.to_dict() for tag in query_tag_of_process(process.id)]
    return process_dict


def app_process_tag_addition(tag_name):
    return add_new_tag(tag_name)


def app_process_tag_delete(tag_id):
    return delete_tag(tag_id=tag_id)


def app_process_tag_upgrade(tag_id, tag_name):
    return edit_tag(tag_id=tag_id, tag_name=tag_name)


def app_process_tags_list():
    tag_list = []
    for tag in query_tags():
        tag_list.append(tag.to_dict())
    return tag_list


def app_get_process_pic(file_url):
    if file_url.startswith('/'):
        file_url = file_url[1:]
    file_url = os.path.join(MEDIA_ROOT, file_url)
    with open(file_url, 'rb') as f:
        image_data = f.read()
    response = HttpResponse(image_data, content_type='image/jpeg')
    response['Content-Disposition'] = 'inline'
    return response
