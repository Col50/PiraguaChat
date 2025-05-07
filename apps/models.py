from django.db import models

class Pregunta(models.Model):
    pregunta = models.CharField(max_length=255)
    informacion = models.TextField()

    def __str__(self):
        return self.pregunta
