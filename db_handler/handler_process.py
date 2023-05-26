from .handler_operation import *
from datetime import datetime


def add_process_ope(process):
    now = datetime.now()
    new_process = Process(
        title=process.get("title"),
        describe=process.get("describe"),
        create_time=now.strftime("%Y-%m-%d %H:%M:%S")
    )
    new_process.save()

    opes = process.get("operations")
    add_operations(opes, new_process.id)
    return new_process.to_dict()


def del_process_ope(process_id):
    try:
        Process.objects.get(id=process_id).delete()
        return '已删除'
    except Process.DoesNotExist:
        return '不存在的process_id'


def update_process_descript(process_id, **kwargs):
    Process.objects.filter(id=process_id).update(**kwargs)
    return True


def query_processes():
    return Process.objects.order_by('-create_time').all().prefetch_related('operation_set')


def query_processes_from_title(title):
    return Process.objects.filter(title__icontains=title).order_by('-create_time').all().prefetch_related('operation_set')


def query_process(process_id):
    return Process.objects.get(id=process_id)
