from django.db import models


class HistorialMensaje(models.Model):
    TIPO_USUARIO_CHOICES = [
        ("persona", "Persona"),
        ("ai", "AI"),
    ]
    numero_celular = models.CharField(max_length=20)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)
    mensaje_respuesta = models.TextField()
    hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_usuario} - {self.numero_celular} - {self.hora}"
