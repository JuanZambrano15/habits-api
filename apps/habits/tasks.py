import logging
from datetime import date
import requests
from celery import shared_task
from django.conf import settings
from .models import Habit, CompletionRecord

logger = logging.getLogger(__name__)


@shared_task
def check_reminders():
    """
    Revisa qué hábitos tienen programado el día de hoy y todavía no
    tienen un registro de cumplimiento creado para hoy. Por cada uno,
    dispara un recordatorio (log + webhook simulado).
    """
    today = date.today()
    weekday_number = today.weekday()  # 0=lunes ... 6=domingo, coincide con nuestro DayOfWeek

    habits_today = Habit.objects.filter(
        is_active=True,
        scheduled_days__number=weekday_number
    ).exclude(
        completion_records__date=today
    )

    for habit in habits_today:
        send_reminder.delay(habit.id)

    logger.info(f"Revisión de recordatorios: {habits_today.count()} hábitos pendientes hoy ({today}).")
    return habits_today.count()


@shared_task
def send_reminder(habit_id):
    """
    Tarea separada por hábito (no todo en una sola tarea gigante):
    si falla el recordatorio de un hábito, no afecta a los demás,
    y Celery puede reintentarla individualmente si configuramos retry.
    """
    habit = Habit.objects.select_related("user").get(id=habit_id)
    message = f"Recordatorio: no olvides '{habit.name}' hoy, {habit.user.username}."

    logger.info(message)

    if settings.REMINDER_WEBHOOK_URL:
        try:
            requests.post(
                settings.REMINDER_WEBHOOK_URL,
                json={"user": habit.user.username, "habit": habit.name, "message": message},
                timeout=5
            )
        except requests.RequestException as e:
            logger.warning(f"No se pudo enviar el webhook para el hábito {habit_id}: {e}")