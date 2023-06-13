import json

from django.http import JsonResponse
from env import *
from .app import *


# 下面接口是操作process
def add_process(request):
    data = json.loads(request.body)
    new_process_dict = app_add_process_and_operation(data)
    return JsonResponse({
        "data": new_process_dict,
        "code": 0
    })


def delete_process(request):
    data = json.loads(request.body)
    msg = app_delete_process_and_ope(data.get("processId"))
    return JsonResponse({
        "code": 0,
        "msg": msg
    })


def update_process(request):
    data = json.loads(request.body)
    new_process_dict = app_update_process_and_operation_and_relation(data)
    return JsonResponse({
        "data": new_process_dict,
        "code": 0
    })


def get_process_list(request):
    data = json.loads(request.body)
    process_dicts = app_process_list(data.get('title'), data.get('tagIds'))
    return JsonResponse({
        "data": process_dicts,
        "code": 0
    })


def get_process_detail(request):
    data = json.loads(request.body)
    process_dict = app_process_detail(data.get('processId'))
    return JsonResponse({
        "data": process_dict,
        "code": 0
    })


# 下面接口是操作process的tag
def add_process_tag(request):
    data = json.loads(request.body)
    app_process_tag_addition(data.get('tagName'))
    return JsonResponse({
        "data": app_process_tags_list(),
        "code": 0
    })


def del_process_tag(request):
    data = json.loads(request.body)
    app_process_tag_delete(data.get('tagId'))
    return JsonResponse({
        "data": app_process_tags_list(),
        "code": 0
    })


def edit_process_tag(request):
    data = json.loads(request.body)
    app_process_tag_upgrade(data.get('tagId'), data.get('tagName'))
    return JsonResponse({
        "data": app_process_tags_list(),
        "code": 0
    })


def get_process_tag(request):
    return JsonResponse({
        "data": app_process_tags_list(),
        "code": 0
    })


# 下面接口是操作process和tag的想关性
def update_process_tag_relation(request):
    data = json.loads(request.body)
    app_update_process_tag_relation(data.get('processId'), data.get('tagIds'))


# 其他接口
def get_tag_list(request):
    return JsonResponse(ALL_TAGS, safe=False)


def get_keyword_list(request):
    return JsonResponse(ALL_BUTTON, safe=False)
