import platform
import threading
import concurrent.futures
import time

from django.http import HttpResponse

from core_handler import runner
import logging
from alert.check_alert import *

logger = logging.getLogger(__name__)


def _request_safari(tags, url, args=None, method='POST'):
    if 'safari' in tags and 'Darwin' != platform.system():
        url = MACOS_URL + url
        if method == 'POST':
            header = {'Content-Type': 'application/json'}
            requests.post(url=url, headers=header, json=args)
            return True
        elif method == 'GET':
            response = requests.get(url=url, params=args)
            return HttpResponse(response)
    return False


def _run_chrome_case(case_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=CHROME_THREADING) as executor:
        futures = [executor.submit(app_run_case, case_id, 0) for case_id in case_list]
        concurrent.futures.wait(futures)


def _run_safari_case(case_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(app_run_case, case_id, 0) for case_id in case_list]
        concurrent.futures.wait(futures)


def app_add_new_cases(data):
    for case in data:
        add_new_case(case, model='chrome')
        add_new_case(case, model='safari')
    return True


def app_delete_case(case_id):
    case = query_case_from_case_id(case_id)
    if _request_safari(case.tags, '/api/case/delCase', {'caseId': case_id}):
        return True
    delete_case(case_id)
    return True


def app_update_case_code(case_id=None, process_id=None):
    if case_id:
        case = query_case_from_case_id(case_id=case_id)
        dic = {"operations": [ope.to_dict() for ope in query_operations(case.process_id)]}
        operations = json.dumps(dic["operations"])
        del_snapshot_direct(case_id)
        if 'safari' in case.tags.split(','):
            code = compiler.CompileCode().compile_code(dic["operations"], 'safari')
        elif 'firefox' in case.tags.split(','):
            code = compiler.CompileCode().compile_code(dic["operations"], 'firefox')
        else:
            code = compiler.CompileCode().compile_code(dic["operations"], 'chrome')
        update_case(case_id, last_succ=0, has_norm=0, code=code, operations=operations)
        return True
    if process_id:
        cases_1 = query_all_cases_from_process_id(process_id)
        cases_2 = query_all_cases_from_relation_process_id(process_id)
        cases = cases_1.union(cases_2)

        for case_id in cases.values_list("id", flat=True):
            app_update_case_code(case_id=case_id)


def app_update_norm_file(case_id):
    case = query_case_from_case_id(case_id)
    if _request_safari(case.tags, '/api/case/updateNorm', {'caseId': case_id}):
        return True
    snapshot_file_mv_current_to_norm(case_id)
    return True


def app_edit_case_tags(data: json):
    case_id = data.get("caseId")
    tags = ','.join([tag for tag in data.get("tag")])
    update_case(case_id, tags=tags)
    return True


def app_initial_case(case_id):
    del_snapshot_direct(case_id)
    update_case(case_id, has_norm=0, last_succ=0, is_running=0, is_waiting=0, run_log='')
    return True


def app_get_case_from_tags(data):
    return get_cases_from_tags(data.get("tags"))


def app_get_all_case():
    return query_all_cases()


def app_get_case_detail(case_id):
    return query_case_from_case_id(case_id).to_dict()


def app_get_case_code(case_id):
    case = query_case_from_case_id(case_id)
    keywords = CODE_INDEX
    data = ''
    for line in case.code.split('\n'):
        line = line.strip()
        if any(keyword in line for keyword in keywords) and '.save_screenshot' not in line:
            data += f'{line}\n'
    return data


def app_get_picture(file_url, model):
    if model == 'safari':
        result = _request_safari(
            tags=model,
            url='/api/case/getPic',
            args={'fileUrl': file_url},
            method='GET'
        )
        return result
    file_url = os.path.join(MEDIA_ROOT, file_url)
    with open(file_url, 'rb') as f:
        image_data = f.read()
    response = HttpResponse(image_data, content_type='image/jpeg')
    response['Content-Disposition'] = 'inline'
    return response


def app_run_case(case_id, is_debug=1):
    case = query_case_from_case_id(case_id)
    if _request_safari(case.tags, '/api/case/runCase', args={'caseId': case_id, 'debug': is_debug}):
        return True

    if 'chrome' in case.tags:
        model = 'chrome'
    else:
        model = 'safari'
    logging.info(f'开始run{case_id}')

    case_file_path = os.path.join(MEDIA_ROOT, "case-records", f"case-{case_id}")
    update_case(case_id, is_running=1)
    run_norm = not bool(case.has_norm)
    has_error, run_log, error_count, camp_time = runner.Run(
        options={
            "caseId": case_id,
            "caseFilePath": case_file_path,
            "runNorm": run_norm
        }
    ).run_case(
        code=case.code,
        model=model
    )
    now = datetime.now()

    has_norm = 1 if not has_error and run_norm else case.has_norm
    last_succ = 2 if has_error or error_count else 1
    logging.info(f'error_count: {error_count}')
    logging.info(f'camp_time: {camp_time}')
    update_case_last_run_result(
        case_id,
        last_error_count=error_count,
        last_comp_count=camp_time,
    )
    update_case(
        case_id,
        has_norm=has_norm,
        last_succ=last_succ,
        last_run_time=now.strftime("%Y-%m-%d %H:%M:%S"),
        run_log=run_log,
        is_running=0
    )

    return True


def app_run_cases_from_tags(tags):
    cases = get_cases_from_tags(tags)
    cases_id_list = [case.id for case in cases]
    for case_id in cases_id_list:
        t = threading.Thread(target=app_run_case, args=(case_id, 0))
        t.start()


def app_run_all_cases():
    cases = query_all_cases()
    time.sleep(300)
    chrome_cases_id_list = [case.id for case in cases if 'chrome' in case.tags]
    safari_cases_id_list = [case.id for case in cases if 'safari' in case.tags]
    thread_chrome = threading.Thread(target=_run_chrome_case, args=(chrome_cases_id_list,))
    thread_safari = threading.Thread(target=_run_safari_case, args=(safari_cases_id_list,))

    thread_chrome.start()
    thread_safari.start()

    thread_chrome.join()
    thread_safari.join()

    logging.info("已跑完所有案例")
    alert_qa()
