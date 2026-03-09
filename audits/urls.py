from django.urls import path
from . import views

app_name = "audits"

urlpatterns = [
    path("", views.audit_list, name="audit_list"),
    path("<int:pk>/", views.audit_detail, name="audit_detail"),
]