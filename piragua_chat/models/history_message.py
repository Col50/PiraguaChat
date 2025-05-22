from django.db import models
from piragua_chat.enum.message_type import MessageType  # Importa el enum


class HistoryMessage(models.Model):

    phone_number = models.CharField(max_length=20)
    user_type = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.value) for tag in MessageType],
    )
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tool_call_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "history_message"

    def __str__(self):
        return f"{self.user_type} - {self.phone_number} - {self.date}"
