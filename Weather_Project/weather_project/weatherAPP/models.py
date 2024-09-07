from django.db import models

class Cityname(models.Model):
    city=models.CharField(max_length=200)
