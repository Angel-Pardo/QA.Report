from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Project, TestCase, Document


admin.site.unregister(Group)

admin.site.register(Project)
admin.site.register(TestCase)
admin.site.register(Document)
