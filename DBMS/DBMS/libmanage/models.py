from django.db import models
from django.contrib.auth.models import User

# Create your models here.

branch_choices=(
    ('cse','CSE'),
    ('ece','ECE'),
)

program_choices=(
    ('ug1','UG1'),
    ('ug2','UG2'),
    ('ug3', 'UG3'),
    ('ug4', 'UG4'),
    ('phd','PHD'),
    ('ms','MS'),

)

section_choices=(
    ('a','A'),
    ('b','B'),
)


class Fullname(models.Model):
    firstname = models.CharField(max_length=255)
    midname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)


class Course(models.Model):
    cname=models.CharField(max_length=150,unique=True)
    #time_allocated

class Student(models.Model):

    rollno=models.CharField( max_length=20, primary_key= True)
    name= models.ForeignKey(Fullname, on_delete=models.CASCADE)
    branch = models.CharField(max_length=10,choices=branch_choices)
    program = models.CharField(max_length=10,choices=program_choices)
    course_taken=models.ManyToManyField(Course,related_name='students')
    section=models.CharField(max_length=10,choices=section_choices)

class Professor(models.Model):
    name=models.CharField(max_length=100)
    teach_course=models.ManyToManyField(Course,related_name='professors')
    dept=models.CharField(max_length=10,choices=branch_choices)




