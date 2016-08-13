from django.db import models


class FreeProxy(models.Model):
    ip = models.CharField(max_length=200)
    working = models.BooleanField(default=True)
    number_of_uses = models.PositiveSmallIntegerField(default=0)
