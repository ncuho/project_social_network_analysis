from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Link(models.Model):
    link = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        to_field='id',
    )

    def __str__(self):
        return self.name
    class Meta:
        ordering = ("id",)

