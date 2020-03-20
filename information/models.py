from django.db import models


class Company(models.Model):
    index = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)