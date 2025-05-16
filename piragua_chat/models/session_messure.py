from django.db import models
from .session import Session
from .messure import Messure


class SessionMessure(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    messure = models.ForeignKey(Messure, on_delete=models.CASCADE)
    user_id = models.DateTimeField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "session_messure"

    def __str__(self):
        return f"Session {self.session.id} - Messure {self.messure.id}"
