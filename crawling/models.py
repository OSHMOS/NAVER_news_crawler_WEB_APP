from django.db import models

# Create your models here.


class Query(models.Model):
    query = models.TextField()
