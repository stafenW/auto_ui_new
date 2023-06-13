from .handler_operation import *


def add_process_ope(title, describe, create_time):
    new_process = Process(
        title=title,
        describe=describe,
        create_time=create_time
    )
    new_process.save()

    return new_process.id


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
    return Process.objects.filter(title__icontains=title).order_by('-create_time').all().prefetch_related(
        'operation_set')


def query_process(process_id):
    return Process.objects.get(id=process_id)


def query_process_from_filter(**kwargs):
    return Process.objects.filter(**kwargs).order_by('-create_time').all().prefetch_related('operation_set')
