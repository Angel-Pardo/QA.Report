from django.urls import path
from . import views

app_name = 'qa'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('testcases/<int:pk>/documents/', views.testcase_documents, name='testcase_documents'),
]