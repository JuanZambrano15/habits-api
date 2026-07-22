from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from apps.habits.models import Habit
from .services import calculate_streak, calculate_completion_percentage
from drf_spectacular.utils import extend_schema, OpenApiExample


class HabitAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary="Resumen analitico de habitos del usuario",
        description="Devuelve la racha actual y el porcentaje de cumplimiento de los ultimos 30 dias, por cada habito activo del usuario autenticado.",
        examples=[
            OpenApiExample(
                "Ejemplo de respuesta",
                value=[{"habit_id": 1, "habit_name": "Tomar agua", "current_streak": 3, "completion_percentage_30d": 66.7}],
                response_only=True,
            )
        ],
    )

    def get(self, request):
        habits = Habit.objects.filter(user=request.user, is_active=True)

        data = [
            {
                "habit_id": habit.id,
                "habit_name": habit.name,
                "current_streak": calculate_streak(habit),
                "completion_percentage_30d": calculate_completion_percentage(habit, days=30),
            }
            for habit in habits
        ]

        return Response(data)
