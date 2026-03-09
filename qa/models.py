from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Project(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="test_cases")
    title = models.CharField(max_length=200)
    test_number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["project", "test_number"], name="uniq_testnumber_per_project")
        ]
        ordering = ["test_number", "title"]

    def __str__(self):
        return f"#{self.test_number} - {self.title}"


class Directory(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="directories")
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, null=True, blank=True, related_name="directories")
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ("project", "test_case", "name")
        ordering = ("name",)


    def __str__(self):
        if self.test_case:
            return f"{self.project.name} / {self.test_case.name} / {self.name}"
        return f"{self.project.name} / {self.name}"



class DocumentCategory(models.TextChoices):
    LOGS_FALLAS = "logs", "Logs importantes de fallas"
    REPORTE_FINAL = "final", "Reporte final"
    EVIDENCIAS = "evidence", "Evidencias"
    ANALISIS = "analysis", "Análisis"
    DOCUMENTACION = "docs", "Documentación del proyecto"
    OTRO = "other", "Otro"


def document_upload_to(instance, filename):
    project = None
    if instance.test_case_id:
        project = instance.test_case.project

    project_part = slugify(project.name) if project else "no-project"

    if instance.directory_id and instance.directory.slug:
        dir_part = instance.directory.slug
    else:
        dir_part = "root"

    return f"projects/{project_part}/{dir_part}/{filename}"


class Document(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.SET_NULL, null=True, blank=True, related_name="documents")
    directory = models.ForeignKey(Directory, on_delete=models.SET_NULL, null=True, blank=True, related_name="documents")
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=DocumentCategory.choices, default=DocumentCategory.OTRO)
    notes = models.TextField(blank=True, default="")
    file = models.FileField(upload_to=document_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_case} - {self.title}"