from django.contrib import admin
from .models import Audit, AuditCriterion, NonConformity, CorrectiveAction


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ("title", "audit_type", "area", "status", "planned_date")
    list_filter = ("audit_type", "status")
    search_fields = ("title", "area", "auditor", "responsible_area")


@admin.register(AuditCriterion)
class AuditCriterionAdmin(admin.ModelAdmin):
    list_display = ("audit", "item_number", "description", "result")
    list_filter = ("audit", "result")
    search_fields = ("description",)


@admin.register(NonConformity)
class NonConformityAdmin(admin.ModelAdmin):
    list_display = ("id", "audit", "nc_type", "status", "responsible")
    list_filter = ("nc_type", "status")
    search_fields = ("description", "responsible")


@admin.register(CorrectiveAction)
class CorrectiveActionAdmin(admin.ModelAdmin):
    list_display = ("non_conformity", "due_date", "completed")
    list_filter = ("completed",)