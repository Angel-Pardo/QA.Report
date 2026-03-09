import django_filters
from django import forms
from django.db.models import Q
from .models import Document

class DocumentFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method="filter_q",
        label="Buscar",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Título o notas"})
    )

    class Meta:
        model = Document
        fields = ["category"]

        filter_overrides = {
            forms.DateField: {"filter_class": django_filters.DateFilter},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "category" in self.form.fields:
            self.form.fields["category"].widget.attrs["class"] = "form-select"

    def filter_q(self, queryset, name, value):
        value = (value or "").strip()
        if not value:
            return queryset
        return queryset.filter(Q(title__icontains=value) | Q(notes__icontains=value))