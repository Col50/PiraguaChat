from django.db import models


class HistoryMessage(models.Model):
    USER_TYPE_CHOICES = [
        ("human", "human"),
        ("ai", "ai"),
        ("tool", "tool"),
        ("system", "system"),
    ]
    phone_number = models.CharField(max_length=20)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tool_call_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "history_message"

    def __str__(self):
        return f"{self.user_type} - {self.phone_number} - {self.date}"
