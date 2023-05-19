from db_handler.handler_process import *


def process_list():
    processes = query_processes()
    process_dicts = []

    for p in processes:
        p_dict = p.to_dict()
        p_dict["operations"] = [ope.to_dict() for ope in p.operation_set.all()]
        process_dicts.append(p_dict)
    return process_dicts


def add_process_and_operation(process):
    return add_process_ope(process)


def update_process_and_operation(process):
    new_process = Process(
        id=process.get("id"),
        title=process.get("title"),
        describe=process.get("describe")
    )
    update_process_descript(process.get("id"), title=process.get("title"), describe=process.get("describe"))
    update_operations(process.get("operations"), process.get("id"))
    return new_process.to_dict()


def process_detail(process_id):
    process = query_process(process_id)
    process_dict = process.to_dict()
    process_dict["operations"] = [ope.to_dict() for ope in query_operations(process_id)]
    return process_dict


def delete_process_and_ope(process_id):
    return del_process_ope(process_id)
