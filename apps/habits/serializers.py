from rest_framework import serializers
from .models import Habit, DayOfWeek, CompletionRecord


class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = ["id", "number", "name"]


class HabitSerializer(serializers.ModelSerializer):
    # PrimaryKeyRelatedField: el cliente envía una lista de IDs de días
    # (ej. [0, 2, 4]), no objetos completos — así se maneja un M2M en DRF.
    scheduled_days = serializers.PrimaryKeyRelatedField(
        queryset=DayOfWeek.objects.all(), many=True
    )

    class Meta:
        model = Habit
        fields = ["id", "name", "description", "scheduled_days", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
        # OJO: "user" NO está en fields. Lo asignamos nosotros en la vista,
        # nunca confiamos en que el cliente lo mande (podría mandar el ID de otro usuario).


class CompletionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletionRecord
        fields = ["id", "habit", "date", "status", "created_at"]
        read_only_fields = ["id", "created_at"]