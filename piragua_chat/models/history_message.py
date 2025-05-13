from django.db import models


class History_Message(models.Model):
    USER_TYPE_CHOICES = [
        ("Human", "Human"),
        ("AI", "AI"),
    ]
    phone_number = models.CharField(max_length=20)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tool_call_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user_type} - {self.phone_number} - {self.date}"
