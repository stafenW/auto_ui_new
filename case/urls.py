from django.urls import path
from . import views

urlpatterns = [
    path('addCases', views.add_cases),
    path('getCaseList', views.get_case_list),
    path('getCaseDetail', views.get_case_detail),
    path('runCase', views.run_case),
    path('runCases', views.run_cases_from_tags),
    path('runAllCases', views.run_all_cases),
    path('delCase', views.del_case),
    path('getPic', views.get_pic),
    path('getCaseCode', views.get_case_code),
    path('updateNorm', views.update_norm),
    path('updateCaseFromC', views.update_case_code_from_cases),
    path('updateCaseFromP', views.update_case_code_from_process),
    path('editCaseTag', views.edit_case_tag),
    path('initialCase', views.case_initial),
    path('getLowestSML', views.get_lowest_similarity)
]
