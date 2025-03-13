from django.db import models

from main_app.choices import EnrollmentGradeType


# class Employee(models.Model):
#     name = models.CharField(max_length=30)
#     email_address = models.EmailField()
#     photo = models.URLField()
#     birth_date = models.DateField()
#     works_full_time = models.BooleanField()
#     created_on = models.DateTimeField(auto_now_add=True)
#
#
# class Department(models.Model):
#
#     class Cities(models.TextChoices):
#         SF = 'SF', 'Sofia'
#         PB = 'PB', 'Plovdiv'
#         BS = 'BS', 'Burgas'
#         V = 'V', 'Varna'
#
#     code = models.CharField(
#         max_length=4,
#         primary_key=True,
#         unique=True
#     )
#     name = models.CharField(
#         max_length=50,
#         unique=True
#     )
#     employees_count = models.PositiveIntegerField(
#         default=1,
#         verbose_name='Employees count'
#     )
#     location = models.CharField(
#         max_length=20,
#         null=True,
#         blank=True,
#         choices=Cities.choices
#     )
#     last_edited_on = models.DateTimeField(auto_now=True, editable=False)


# class Project(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(null=True, blank=True)
#     budget = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
#     duration_in_days = models.PositiveIntegerField(null=True, blank=True, verbose_name='Duration in Days')
#     estimated_hours = models.FloatField(null=True, blank=True, verbose_name='Estimated Hours')
#     start_date = models.DateField(verbose_name='Start Date', null=True, blank=True, default=date.today())
#     created_on = models.DateTimeField(auto_now_add=True, editable=False)
#     last_edited_on = models.DateTimeField(auto_now=True, editable=False)


class Lecturer(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    name = models.CharField(
        max_length=100
    )
    code = models.CharField(
        max_length=10
    )
    lecturer = models.ForeignKey(
        to='Lecturer',
        on_delete=models.CASCADE
    )


class Student(models.Model):
    student_id = models.CharField(
        max_length=10,
        primary_key=True
    )
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    birth_date = models.DateField()
    email = models.EmailField(
        unique=True
    )
    subjects = models.ManyToManyField(to='Subject', through='StudentEnrollment')


class StudentEnrollment(models.Model):
    student = models.ForeignKey(
        to='Student',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        to='Subject',
        on_delete=models.CASCADE
    )
    enrollment_date = models.DateField()
    grade = models.CharField(
        max_length=1,
        choices=EnrollmentGradeType

    )






