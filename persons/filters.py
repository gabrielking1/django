import django_filters
from persons.models import *
from django import forms


class ProjectFilter(django_filters.FilterSet):
    # level = django_filters.MultipleChoiceFilter(choices=Student.LevelChoices.choices,
    # widget = forms.CheckboxSelectMultiple)
    class Meta:
        model = Student
        
        fields = {
            'title' : ['icontains'],
            'year' : ['exact'],
            'level' :['exact'],
            'department' :['exact']
        }