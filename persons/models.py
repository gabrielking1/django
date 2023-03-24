from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Faculty(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Student(models.Model):
    class LevelChoices(models.TextChoices):
        ND = "ND"
        HND = "HND"
    name = models.CharField(max_length=300)
    supervisor = models.CharField(max_length=50)
    title = models.CharField(max_length=125)
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1895),
            MaxValueValidator(2050),
        ]
    )
    level = models.CharField(max_length=4, choices=LevelChoices.choices)
    date = models.DateField(auto_now = True)
    file = models.FileField(upload_to='documents/')
    source_code = models.FileField(upload_to = "source/")
    name = models.CharField(max_length=124)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name