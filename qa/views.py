from django.shortcuts import render, get_object_or_404
from .models import Project, TestCase, Document

def project_list(request):
    projects = Project.objects.order_by('name')
    return render(request, 'qa/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    test_cases = TestCase.objects.filter(project=project).order_by('title')
    return render(request, 'qa/project_detail.html', {
        'project': project,
        'testcases': test_cases,

    })

def testcase_documents(request, pk):
    testcase = get_object_or_404(TestCase, pk=pk)
    documents = Document.objects.filter(test_case=testcase).order_by('-created_at', 'title')
    return render(request, 'qa/testcase_documents.html', {
        'testcase': testcase,
        'documents': documents,
    })