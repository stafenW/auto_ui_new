from django.urls import path
from . import views

urlpatterns = [
    path('getProcessList', views.get_process_list),
    path('getProcessDetail', views.get_process_detail),
    path('addProcess', views.add_process),
    path('deleteProcess', views.delete_process),
    path('updateProcess', views.update_process),
    path('getTagList', views.get_tag_list),
    path('getButtonList', views.get_keyword_list),
    path('addProcessTag', views.add_process_tag),
    path('delProcessTag', views.del_process_tag),
    path('editProcessTag', views.edit_process_tag),
    path('getProcessTag', views.get_process_tag),
    path('updateProcessTagRelation', views.update_process_tag_relation)
]
