from django.db import models
from django.utils import timezone


def audit_evidence_upload_to(instance, filename):
    audit_id = instance.audit.id if hasattr(instance, "audit") and instance.audit_id else "sin-auditoria"
    return f"audits/audit_{audit_id}/{filename}"


class AuditType(models.TextChoices):
    INTERNA = "interna", "Interna"
    EXTERNA = "externa", "Externa"


class AuditStatus(models.TextChoices):
    PROGRAMADA = "programada", "Programada"
    EN_PROCESO = "en_proceso", "En proceso"
    CERRADA = "cerrada", "Cerrada"


class CriterionResult(models.TextChoices):
    CUMPLE = "cumple", "Cumple"
    NO_CUMPLE = "no_cumple", "No cumple"
    OBSERVACION = "observacion", "Observación"


class NonConformityType(models.TextChoices):
    MAYOR = "mayor", "Mayor"
    MENOR = "menor", "Menor"
    OBSERVACION = "observacion", "Observación"


class NonConformityStatus(models.TextChoices):
    ABIERTA = "abierta", "Abierta"
    EN_PROCESO = "en_proceso", "En proceso"
    CERRADA = "cerrada", "Cerrada"


class Audit(models.Model):
    title = models.CharField(max_length=200)
    audit_type = models.CharField(max_length=20, choices=AuditType.choices)
    area = models.CharField(max_length=150)
    objective = models.TextField(blank=True, default="")
    planned_date = models.DateField()
    execution_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=AuditStatus.choices,
        default=AuditStatus.PROGRAMADA
    )
    auditor = models.CharField(max_length=150, blank=True, default="")
    responsible_area = models.CharField(max_length=150, blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ("-created_at", "title")

    def __str__(self):
        return f"{self.title} - {self.get_audit_type_display()}"


class AuditCriterion(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name="criteria")
    item_number = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    result = models.CharField(
        max_length=20,
        choices=CriterionResult.choices,
        default=CriterionResult.OBSERVACION
    )
    observation = models.TextField(blank=True, default="")

    class Meta:
        ordering = ("item_number",)
        unique_together = ("audit", "item_number")

    def __str__(self):
        return f"{self.audit.title} - Criterio {self.item_number}"


class NonConformity(models.Model):
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name="non_conformities")
    criterion = models.ForeignKey(
        AuditCriterion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="non_conformities"
    )
    nc_type = models.CharField(max_length=20, choices=NonConformityType.choices)
    description = models.TextField()
    evidence = models.TextField(blank=True, default="")
    responsible = models.CharField(max_length=150)
    status = models.CharField(
        max_length=20,
        choices=NonConformityStatus.choices,
        default=NonConformityStatus.ABIERTA
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"NC #{self.id} - {self.get_nc_type_display()}"


class CorrectiveAction(models.Model):
    non_conformity = models.OneToOneField(
        NonConformity,
        on_delete=models.CASCADE,
        related_name="corrective_action"
    )
    root_cause = models.TextField()
    immediate_action = models.TextField()
    permanent_action = models.TextField()
    evidence = models.TextField(blank=True, default="")
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f"Acción correctiva NC #{self.non_conformity.id}"