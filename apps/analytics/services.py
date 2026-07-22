from datetime import date, timedelta


def calculate_streak(habit):
    """
    Cuenta días consecutivos completados, retrocediendo desde hoy.
    Los días en que el hábito NO estaba programado se saltan sin romper
    la racha (si tu hábito es solo lunes/miércoles/viernes, el martes no cuenta).
    La racha se rompe en el primer día programado que falta o no está completado.
    """
    scheduled_numbers = set(habit.scheduled_days.values_list("number", flat=True))
    if not scheduled_numbers:
        return 0

    streak = 0
    today = date.today()

    for offset in range(365):  # tope de un año hacia atrás, evita loop infinito
        day = today - timedelta(days=offset)
        if day.weekday() not in scheduled_numbers:
            continue

        record = habit.completion_records.filter(date=day).first()
        if record and record.status == "completed":
            streak += 1
        else:
            break

    return streak


def calculate_completion_percentage(habit, days=30):
    """
    % de cumplimiento sobre los últimos `days` días, contando solo
    los días en que el hábito estaba programado (no penaliza días
    en que ni siquiera aplicaba cumplirlo).
    """
    scheduled_numbers = set(habit.scheduled_days.values_list("number", flat=True))
    if not scheduled_numbers:
        return 0.0

    today = date.today()
    start = today - timedelta(days=days - 1)

    scheduled_dates = [
        start + timedelta(days=i)
        for i in range(days)
        if (start + timedelta(days=i)).weekday() in scheduled_numbers
        and (start + timedelta(days=i)) <= today
    ]

    if not scheduled_dates:
        return 0.0

    completed_count = habit.completion_records.filter(
        date__in=scheduled_dates, status="completed"
    ).count()

    return round((completed_count / len(scheduled_dates)) * 100, 1)