from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from apps.habits.models import Habit
from .services import calculate_streak, calculate_completion_percentage


class HabitAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
