from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4

# Create your models here.
class Subject(models.Model):
    uid = models.UUIDField(default=uuid4, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    uid = models.UUIDField(default=uuid4, unique=True)
    name = models.CharField(max_length=30)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Room(models.Model):
    uid = models.UUIDField(default=uuid4, unique=True)
    name = models.CharField(max_length=5)
    strength = models.IntegerField()
    group = models.IntegerField()

    def __str__(self):
        return self.name

class Link(models.Model):
    uid = models.UUIDField(default=uuid4, unique=True)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.room.name} ({self.teacher.name})'
    

class Entry(models.Model):
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    date = models.DateField()
    absent = models.CharField(max_length=30, blank=True, null=True)