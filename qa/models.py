from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_cases')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Directory(models.Model):
    name = models.CharField(max_length=120, help_text='Nombre del directorio')
    
    test_case = models.ForeignKey(
        'qa.TestCase',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='directories',
        help_text='Al que pertenece este directorio.'
    )

    def __str__(self):
        return self.name


class Document(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
