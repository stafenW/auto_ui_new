from datetime import datetime

from django.db.models import Count

from .models import Operation
from .models import Process


def add_operation(ope, index, process_id):
    ope_type = ope.get("operation")
    value = ope.get("value")
    now = datetime.now()
    new_ope = Operation(
        create_time=now.strftime("%Y-%m-%d %H:%M:%S"),
        ope_type=ope_type,
        process_id=Process(id=process_id),
        process_index=index,
        ope_name=ope.get("opeName")
    )

    if ope_type == "open-page":
        new_ope.set_open_url(value.get("url"))
    elif ope_type == "jump":
        new_ope.set_open_url(value.get("url"))
    elif ope_type == "click":
        new_ope.set_finder(value.get("elFinder"))
    elif ope_type == "try-to-click":
        new_ope.set_finder(value.get("elFinder"))
    elif ope_type == "input":
        new_ope.set_finder(value.get("elFinder"))
        new_ope.set_input_val(value.get("inputVal"), value.get("isEnter"))
    elif ope_type == "wait":
        new_ope.set_time_limit(value.get("timeLimit"))
    elif ope_type == "wait-el":
        new_ope.set_finder(value.get("elFinder"))
        new_ope.set_time_limit(value.get("timeLimit"))
    elif ope_type == "snapshot":
        new_ope.set_var_ope(value.get("varOpe"))
    elif ope_type == "snapshot-el":
        new_ope.set_finder(value.get("elFinder"))
        new_ope.set_var_ope(value.get("varOpe"))
    elif ope_type == "get-text":
        new_ope.set_finder(value.get("elFinder"))
        new_ope.set_var_ope(value.get("varOpe"))
        new_ope.set_comp_var(value.get("compVar"))
    elif ope_type == "other-process":
        new_ope.set_other_process(value.get("otherProcessId"))
    elif ope_type == "keyword-opt":
        new_ope.set_finder(value.get("elFinder"))
        new_ope.set_keyword_opt(value.get('keywordOpt'))
    new_ope.save()
    return True


def add_operations(opes, process_id):
    for index, ope in enumerate(opes):
        add_operation(ope, index, process_id)
    return True


def del_operations(process_id):
    Operation.objects.filter(process_id=process_id).delete()
    return True


def update_operations(opes, process_id):
    del_operations(process_id)
    add_operations(opes, process_id)
    return True


def query_operations(process_id):
    return Operation.objects.filter(process_id=process_id).order_by("process_index")


def query_process_id_from_other_process(other_process):
    return Operation.objects.filter(other_process=other_process).values('process_id')


def query_operations_count(process_id):
    return Operation.objects.filter(process_id=process_id).count()


def query_operations_count_to_dict(process_ids):
    operation_counts = Operation.objects.filter(process_id__in=process_ids).values('process_id').annotate(
        count=Count('id'))
    count_dict = {item['process_id']: item['count'] for item in operation_counts}

    return count_dict
