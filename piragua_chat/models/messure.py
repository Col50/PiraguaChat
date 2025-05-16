from random import sample
from django.db import models


class Messure(models.Model):
    user_id = models.IntegerField()
    meter_id = models.IntegerField()
    date = models.CharField(max_length=255, null=True, blank=True)
    sample = models.CharField(max_length=255, null=True, blank=True)
    observation = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Session {self.session.id} - Messure {self.messure.id}"
