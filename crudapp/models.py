from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name

def get_default_course():
    return Course.objects.get_or_create(name="Default Course", code="DEF101")[0].id

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students', default=get_default_course)

    def __str__(self):
        return self.name
