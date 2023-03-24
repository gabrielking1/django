from django.contrib import admin

# Register your models here.
from .models import Department, Faculty, Student

admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Student)