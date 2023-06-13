from db_handler.handler_process import *
from db_handler.handler_process_tag import *
from db_handler.handler_process_relate_tag import *


def app_process_list(title='', tag_ids=None):
    if title and tag_ids:
        process_id_list = query_process_id_list_from_tag(tag_ids)
        processes = query_process_from_filter(title__icontains=title, id__in=process_id_list)
    elif title and not tag_ids:
        processes = query_process_from_filter(title__icontains=title)
    elif not title and tag_ids:
        process_id_list = query_process_id_list_from_tag(tag_ids)
        processes = query_process_from_filter(id__in=process_id_list)
    else:
        processes = query_process_from_filter()

    process_dicts = []
    for p in processes:
        p_dict = p.to_dict()
        p_dict["operations"] = [ope.to_dict() for ope in p.operation_set.all()]
        process_dicts.append(p_dict)
    return process_dicts


def app_add_process_and_operation(process):
    title = process.get("title")
    describe = process.get("describe")
    ope_list = process.get("operations")
    tag_list = process.get("tagIds")
    img = process.get("image")

    now = datetime.now()
    create_time = now.strftime("%Y-%m-%d %H:%M:%S")
    new_process_id = add_process_ope(title, describe, create_time)

    add_operations(ope_list, new_process_id)
    add_relates(tag_list, new_process_id)
    return query_process(new_process_id).to_dict()


def app_update_process_and_operation_and_relation(process):
    process_id = process.get("id")
    process_title = process.get("title")
    process_description = process.get("describe")
    process_operation_list = process.get("operations")
    process_tag_list = process.get("tagIds")

    update_process_descript(process_id, title=process_title, describe=process_description)
    update_operations(process_operation_list, process_id)
    update_relation(process_id, process_tag_list)
    return query_process(process_id).to_dict()


def app_update_process_tag_relation(process_id, tag_ids):
    update_relation(process_id, tag_ids)
    return True


def app_process_detail(process_id):
    process = query_process(process_id)
    process_dict = process.to_dict()
    process_dict["operations"] = [ope.to_dict() for ope in query_operations(process_id)]
    return process_dict


def app_delete_process_and_ope(process_id):
    return del_process_ope(process_id)


def app_process_tag_addition(tag_name):
    add_new_tag(tag_name)
    return True


def app_process_tag_delete(tag_id):
    delete_tag(tag_id=tag_id)
    return True


def app_process_tag_upgrade(tag_id, tag_name):
    edit_tag(tag_id=tag_id, tag_name=tag_name)
    return True


def app_process_tags_list():
    tag_list = []
    for tag in query_tags():
        tag_list.append(tag.to_dict())
    return tag_list
