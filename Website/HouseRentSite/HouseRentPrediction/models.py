from django.db import models


# Create your models here.
class Data(models.Model):
    address = models.CharField(max_length=30)
    size = models.IntegerField(max_length=30)
