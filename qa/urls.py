from django.urls import path
from . import views

app_name = "qa"

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("testcases/<int:pk>/documents/", views.testcase_documents, name="testcase_documents"),
    path("testcases/<int:test_case_pk>/documents/upload/", views.document_create, name="document_create"),
    path("documents/<int:pk>/edit/", views.document_update, name="document_update"),
    path("documents/<int:pk>/delete/", views.document_delete, name="document_delete"),
]