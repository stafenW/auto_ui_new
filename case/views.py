from django.http import JsonResponse
from .app import *

BASE_DIR = settings.BASE_DIR


def add_cases(request):
    data = json.loads(request.body)
    app_add_new_cases(data)
    return JsonResponse({
        "code": 0
    })


def del_case(request):
    data = json.loads(request.body)
    app_delete_case(data.get('caseId'))
    return JsonResponse({
        "code": 0
    })


def update_case_code_from_cases(request):
    data = json.loads(request.body)
    app_update_case_code(case_id=data.get('caseId'))
    return JsonResponse({
        "code": 0
    })


def update_case_code_from_process(request):
    data = json.loads(request.body)
    app_update_case_code(process_id=data.get('processId'))
    return JsonResponse({
        "code": 0
    })


def update_norm(request):
    data = json.loads(request.body)
    app_update_norm_file(data.get('caseId'))
    return JsonResponse({
        "code": 0,
        "msg": "update成功"
    })


def edit_case_tag(request):
    data = json.loads(request.body)
    app_edit_case_tags(data)
    return JsonResponse({
        "code": 0,
        "msg": "update成功"
    })


def case_initial(request):
    data = json.loads(request.body)
    app_initial_case(data.get("caseId"))
    return JsonResponse({
        "code": 0,
        "msg": "初始化成功"
    })


def get_case_list(request):
    data = json.loads(request.body)
    if data.get("tags"):
        case_list = app_get_case_from_tags(data)
    else:
        case_list = app_get_all_case()

    return JsonResponse({
        "data": [case.to_dict() for case in case_list],
        "code": 0
    })


def get_case_detail(request):
    data = json.loads(request.body)
    case = app_get_case_detail(data.get("caseId"))
    return JsonResponse({
        "data": case,
        "code": 0
    })


def get_case_code(request):
    data = json.loads(request.body)
    case_id = data.get("caseId")
    data = app_get_case_code(case_id)
    return JsonResponse({
        "data": data,
        "code": 0
    })


def get_pic(request):
    file_url = request.GET.get('fileUrl', '')
    model = request.GET.get('model')
    if file_url == "":
        return HttpResponse("need param 'fileUrl'")
    response = app_get_picture(file_url, model)
    return response


def run_case(request):
    data = json.loads(request.body)
    has_error = app_run_case(data.get("caseId"), data.get("debug"))
    return JsonResponse({
        "code": 0 if has_error else 1
    })


def run_cases_from_tags(request):
    data = json.loads(request.body)
    app_run_cases_from_tags(data.get("tags"))
    return JsonResponse({
        "code": 0
    })


def run_all_cases(request):
    app_run_all_cases()
    return JsonResponse({
        "code": 0
    })
