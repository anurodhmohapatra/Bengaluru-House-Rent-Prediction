from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Data(models.Model):
    address = models.CharField(max_length=30)
    size = models.IntegerField(max_length=30)
    date_posted = models.DateTimeField(timezone.now, default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.address
