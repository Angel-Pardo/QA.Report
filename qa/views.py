from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .filters import DocumentFilter
from .forms import DocumentForm
from .models import Document, Project, TestCase


@login_required
def project_list(request):
    projects = Project.objects.order_by("name")
    return render(request, "qa/project_list.html", {"projects": projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    test_cases = TestCase.objects.filter(project=project).order_by("test_number", "title")
    recent_docs = (
        Document.objects.filter(test_case__project=project)
        .select_related("test_case")
        .order_by("-created_at")[:10]
    )

    return render(
        request,
        "qa/project_detail.html",
        {
            "project": project,
            "test_cases": test_cases,
            "recent_docs": recent_docs,
        },
    )


@login_required
def testcase_documents(request, pk):
    test_case = get_object_or_404(TestCase, pk=pk)
    qs = (
        Document.objects.filter(test_case=test_case)
        .select_related("test_case", "directory")
        .order_by("-created_at")
    )
    f = DocumentFilter(request.GET, queryset=qs)

    return render(
        request,
        "qa/testcase_documents.html",
        {
            "test_case": test_case,
            "filter": f,
            "documents": f.qs,
        },
    )


@login_required
def document_create(request, test_case_pk):
    test_case = get_object_or_404(TestCase, pk=test_case_pk)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.test_case = test_case
            doc.save()
            return redirect("qa:testcase_documents", pk=test_case.pk)
    else:
        form = DocumentForm()

    return render(
        request,
        "qa/document_form.html",
        {
            "test_case": test_case,
            "form": form,
        },
    )


@login_required
def document_update(request, pk):
    doc = get_object_or_404(Document, pk=pk)

    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return redirect("qa:testcase_documents", pk=doc.test_case.pk)
    else:
        form = DocumentForm(instance=doc)

    return render(
        request,
        "qa/document_form.html",
        {
            "test_case": doc.test_case,
            "form": form,
            "doc": doc,
        },
    )


@login_required
def document_delete(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    tc_pk = doc.test_case.pk if doc.test_case else None

    if request.method == "POST":
        doc.delete()
        if tc_pk:
            return redirect("qa:testcase_documents", pk=tc_pk)
        return redirect("qa:project_list")

    return render(request, "qa/document_confirm_delete.html", {"doc": doc})