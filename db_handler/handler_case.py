from .models import Case
import json
from selenium_handler import compiler
from django.utils import timezone
from file_handler.handler_file import *
from .handler_operation import *


def add_new_case(case: json, model='chrome'):
    now = timezone.make_aware(datetime.now())
    new_case = Case(
        process_id=case.get("id"),
        title=case.get("caseTitle"),
        tags=','.join(case.get("tag", [])) + f',{model}' if case.get("tag") else model,
        code=compiler.compile_code(case.get("operations"), model),
        operations=json.dumps(case.get("operations")),
        create_time=now.strftime("%Y-%m-%d %H:%M:%S")
    )
    new_case.save()
    add_file(new_case.id)


def delete_case(case_id):
    Case.objects.get(id=case_id).delete()
    del_file(case_id)


def update_case(case_id, **kwargs):
    Case.objects.filter(id=case_id).update(**kwargs)


def update_case_last_succ(case_id, last_succ=0):
    Case.objects.filter(id=case_id).update(last_succ=last_succ)


def update_case_tag(case_id, tag=''):
    Case.objects.filter(id=case_id).update(tag=tag)


def update_case_last_run_result(case_id, last_comp_count=0, last_error_count=0):
    now = datetime.now()
    Case.objects.filter(id=case_id).update(
        last_run_time=now.strftime("%Y-%m-%d %H:%M:%S"),
        last_comp_count=last_comp_count,
        last_error_count=last_error_count
    )


def query_all_cases():
    return Case.objects.all().order_by("-create_time")


def query_case_from_case_id(case_id):
    return Case.objects.get(id=case_id)


def query_all_cases_from_process_id(process_id):
    return Case.objects.filter(process_id=process_id)


def query_all_cases_from_tag(tag):
    return Case.objects.filter(tags__icontains=tag)


def query_all_cases_values(*args):
    return Case.objects.values(args)


def get_cases_from_tags(tags):
    cases = query_all_cases()
    return [case for case in cases if any(tag in tags for tag in case.tags.split(','))]


def query_all_cases_from_relation_process_id(id):
    def find_process_ids_recursive(process_id, result):
        operations = Operation.objects.filter(other_process=process_id)
        for operation in operations:
            result.append(operation.process_id_id)
            find_process_ids_recursive(operation.process_id_id, result)

    result = []
    find_process_ids_recursive(id, result)
    result = list(set(result))

    return Case.objects.filter(process_id__in=result)
