from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=40)
    ip = models.CharField(max_length=40)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=14, blank=True, null=True)
    type = models.CharField(max_length=3)
    port = models.IntegerField(blank=True, null=True, default='22')

    