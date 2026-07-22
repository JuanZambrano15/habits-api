import pytest
from datetime import date, timedelta
from apps.habits.factories import HabitFactory, CompletionRecordFactory
from apps.habits.models import DayOfWeek
from apps.analytics.services import calculate_streak, calculate_completion_percentage

pytestmark = pytest.mark.django_db  # habilita acceso a la base para todo el archivo


def test_streak_is_zero_with_no_records():
    habit = HabitFactory()
    habit.scheduled_days.set(DayOfWeek.objects.filter(number=date.today().weekday()))
    assert calculate_streak(habit) == 0


def test_streak_counts_consecutive_completed_days():
    habit = HabitFactory()
    today = date.today()
    habit.scheduled_days.set(DayOfWeek.objects.all())  # programado todos los dias, simplifica el test

    for i in range(3):
        CompletionRecordFactory(habit=habit, date=today - timedelta(days=i), status="completed")

    assert calculate_streak(habit) == 3


def test_streak_breaks_on_missed_day():
    habit = HabitFactory()
    today = date.today()
    habit.scheduled_days.set(DayOfWeek.objects.all())

    CompletionRecordFactory(habit=habit, date=today, status="completed")
    CompletionRecordFactory(habit=habit, date=today - timedelta(days=1), status="missed")
    CompletionRecordFactory(habit=habit, date=today - timedelta(days=2), status="completed")

    assert calculate_streak(habit) == 1  # se corta en el dia "missed", no cuenta el de hace 2 dias


def test_completion_percentage_calculation():
    habit = HabitFactory()
    today = date.today()
    habit.scheduled_days.set(DayOfWeek.objects.all())

    CompletionRecordFactory(habit=habit, date=today, status="completed")
    CompletionRecordFactory(habit=habit, date=today - timedelta(days=1), status="missed")

    percentage = calculate_completion_percentage(habit, days=2)
    assert percentage == 50.0