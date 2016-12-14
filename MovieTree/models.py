from django.db import models

class Survey(models.Model):
    question_asked = models.CharField(max_length=200)
    answer_given = models.CharField(max_length=200)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_keyword = models.CharField(max_length=200, default="null")