from django.shortcuts import render, get_object_or_404
from .models import Project, TestCase, Directory


def project_list(request):
    projects = Project.objects.all().order_by("name")
    return render(request, "qa/project_list.html", {"projects": projects})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    test_cases = TestCase.objects.filter(project=project).order_by("title")
    return render(request, "qa/project_detail.html", {"project": project, "test_cases": test_cases})
