from django.urls import path
from . import views

urlpatterns = [
    path('getProcessList', views.get_process_list),
    path('getProcessDetail', views.get_process_detail),
    path('addProcess', views.add_process),
    path('deleteProcess', views.delete_process),
    path('updateProcess', views.update_process),
    path('getTagList', views.get_tag_list),
    path('getBottonList', views.get_keyword_list)
]