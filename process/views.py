import json

from django.http import JsonResponse
from env import *
from .app import *


def add_process(request):
    data = json.loads(request.body)
    new_process_dict = add_process_and_operation(data)
    return JsonResponse({
        "data": new_process_dict,
        "code": 0
    })


def get_process_list(request):
    process_dicts = process_list()
    return JsonResponse({
        "data": process_dicts,
        "code": 0
    })


def get_process_detail(request):
    data = json.loads(request.body)
    process_dict = process_detail(data.get('processId'))
    return JsonResponse({
        "data": process_dict,
        "code": 0
    })


def delete_process(request):
    data = json.loads(request.body)
    msg = delete_process_and_ope(data.get("processId"))
    return JsonResponse({
        "code": 0,
        "msg": msg
    })


def update_process(request):
    data = json.loads(request.body)
    new_process_dict = update_process_and_operation(data)
    return JsonResponse({
        "data": new_process_dict,
        "code": 0
    })


def get_tag_list(request):
    return JsonResponse(ALL_TAGS, safe=False)


def get_keyword_list(request):
    return JsonResponse(ALL_BUTTON, safe=False)
