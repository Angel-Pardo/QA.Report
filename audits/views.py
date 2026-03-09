from django.shortcuts import render, get_object_or_404
from .models import Audit


def audit_list(request):
    audits = Audit.objects.all().order_by("-created_at")
    return render(request, "audits/audit_list.html", {"audits": audits})


def audit_detail(request, pk):
    audit = get_object_or_404(Audit, pk=pk)
    return render(request, "audits/audit_detail.html", {"audit": audit})