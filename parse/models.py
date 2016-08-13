from django.db import models


class Site(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    page = models.PositiveSmallIntegerField()
    date_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
