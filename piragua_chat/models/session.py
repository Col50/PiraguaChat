from django.db import models


class Session(models.Model):
    phone_number = models.CharField(max_length=20)
    last_message_datetime = models.DateTimeField()
    last_notification_datetime = models.DateTimeField()

    def __str__(self):
        return self.phone_number
