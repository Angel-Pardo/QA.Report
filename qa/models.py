from django.db import models
from django.test import TestCase


class Project(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Directory(models.Model):
    
 project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='directios', help_text='Proyecto al que pertenece este directorio')
 test_case = models.ForeignKey(TestCase,on_delete=models.CASCADE,null=True, blank=True, related_name='directios', help_text='al que pertenece este directorio.')
 name = models.CharField(max_length=120,help_text='Nombre del directorio')



class TestCase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Document(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


    
    