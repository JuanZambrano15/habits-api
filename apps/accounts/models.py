from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extiende el usuario por defecto de Django.
    Guardamos la zona horaria para que, en la Fase 4, el job de recordatorios
    pueda calcular la hora correcta de cada usuario en vez de asumir UTC para todos.
    """
    timezone = models.CharField(
        max_length=50,
        default="America/Bogota",
        help_text="Zona horaria del usuario, usada para calcular cuándo enviar recordatorios."
    )

    def __str__(self):
        return self.username
