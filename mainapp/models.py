from django.db import models
from django.contrib.auth.models import User

class Dictionary(models.Model):
	original = models.CharField(max_length = 200)
	translation = models.CharField(max_length = 200)
	soundFileName = models.CharField(max_length = 200)

class UserWords(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	word = models.ForeignKey(Dictionary, on_delete = models.CASCADE)

class WordForms(models.Model):
	word = models.ForeignKey(Dictionary, on_delete = models.CASCADE)
	form = models.CharField(max_length = 200)