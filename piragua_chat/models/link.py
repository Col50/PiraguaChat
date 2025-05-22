from django.db import models


class Link(models.Model):
    name = models.CharField(max_length=255)
    link = models.TextField()

    def __str__(self):
        return self.name
