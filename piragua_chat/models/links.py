from django.db import models


class Links(models.Model):
    nombre = models.CharField(max_length=255)
    enlace = models.TextField()

    def __str__(self):
        return self.nombre
