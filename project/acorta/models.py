from django.db import models

# Create your models here.

class Urls(models.Model):
	url_acortada = models.CharField(max_length=500)
	url_completa = models.CharField(max_length=500)

	def __str__(self):
		return self.url_completa
