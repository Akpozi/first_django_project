from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    # ...
    def __str__(self):
        return self.search

    # ...
    def was_published_recently(self):
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        now = timezone.now()
        # return now - datetime.timedelta(days=1) <= self.pub_date <= now
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    class Meta:
        verbose_name_plural = 'Searches'
