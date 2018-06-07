from django.db import models
from django.contrib.auth.models import User

class Dictionary(models.Model):
	original = models.CharField(max_length = 1024)

class Translation(models.Model):
	translation = models.CharField(max_length = 1024)
	notes = models.CharField(max_length = 200)
	original = models.ForeignKey(Dictionary, on_delete = models.CASCADE)

class WordForms(models.Model):
	word = models.ForeignKey(Dictionary, on_delete = models.CASCADE)
	form = models.CharField(max_length = 200)

class ModernDictionary(models.Model):
	original = models.CharField(max_length = 1024)

class ModernTranslation(models.Model):
	translation = models.CharField(max_length = 1024)
	notes = models.CharField(max_length = 200)
	original = models.ForeignKey(ModernDictionary, on_delete = models.CASCADE)

class UniversalDictionary(models.Model):
	original = models.CharField(max_length = 1024)

class UniversalTranslation(models.Model):
	translation = models.CharField(max_length = 1024)
	notes = models.CharField(max_length = 200)
	original = models.ForeignKey(UniversalDictionary, on_delete = models.CASCADE)	

class UserWords(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	translation = models.ForeignKey(UniversalTranslation, on_delete = models.CASCADE, default = 1)	

class UniversalSounds(models.Model):
	soundfile = models.CharField(max_length = 200)
	original = models.ForeignKey(UniversalDictionary, on_delete = models.CASCADE)	