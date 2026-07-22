from django.db import models
from django.conf import settings


class DayOfWeek(models.Model):
    """
    Catálogo fijo de días de la semana (0=lunes ... 6=domingo).
    Es una tabla, no un choices field, porque la relacionamos con Habito
    mediante ManyToMany: un hábito puede tener varios días, y cada día
    es compartido por muchos hábitos.
    """
    number = models.PositiveSmallIntegerField(unique=True)  # 0-6
    name = models.CharField(max_length=10)  # "Lunes", "Martes", ...

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return self.name


class Habit(models.Model):
    """
    Un hábito le pertenece a un usuario (ForeignKey = relación 1:N).
    on_delete=CASCADE: si se borra el usuario, se borran sus hábitos —
    tiene sentido de negocio, un hábito no existe sin su dueño.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    scheduled_days = models.ManyToManyField(DayOfWeek, related_name="habits")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class CompletionRecord(models.Model):
    """
    Un registro por día por hábito. unique_together evita que se puedan
    crear dos registros para el mismo hábito en la misma fecha
    (equivalente a una restricción UNIQUE compuesta en SQL puro).
    """
    class Status(models.TextChoices):
        COMPLETED = "completed", "Completado"
        SKIPPED = "skipped", "Saltado"
        MISSED = "missed", "Perdido"

    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="completion_records"
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("habit", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {self.status}"