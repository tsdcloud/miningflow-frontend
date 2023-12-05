from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profil(models.Model):
    access = models.TextField()
    refresh = models.TextField()
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='profil')
