from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class Exam(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    options = models.JSONField(null=True, blank=True)
    correct_answer = models.CharField(max_length=255)
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
