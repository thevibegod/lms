from django.db import models
from contests.models import Domain


class Profile(models.Model):
    STUDENT = 0
    INSTRUCTOR = 1
    TYPE_CHOICES = ((STUDENT, 'Student'), (INSTRUCTOR, 'Instructor'))
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    type = models.IntegerField(choices=TYPE_CHOICES)
    domains = models.ManyToManyField(Domain)
