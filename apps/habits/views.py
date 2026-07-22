from rest_framework import viewsets, permissions
from .models import Habit, DayOfWeek, CompletionRecord
from .serializers import HabitSerializer, DayOfWeekSerializer, CompletionRecordSerializer


class DayOfWeekViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet: solo expone list/retrieve, no create/update/delete.
    Tiene sentido porque es un catálogo fijo — nadie debería poder crear
    "octavo día de la semana" desde la API.
    """
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer
    permission_classes = [permissions.IsAuthenticated]


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # CLAVE DE SEGURIDAD: solo devolvemos los hábitos del usuario autenticado,
        # nunca Habit.objects.all(). self.request.user viene del token/sesión.
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Aquí asignamos el dueño del hábito del lado del servidor,
        # exactamente lo que mencionamos que el serializer no debe confiar del cliente.
        serializer.save(user=self.request.user)


class CompletionRecordViewSet(viewsets.ModelViewSet):
    serializer_class = CompletionRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Mismo principio: solo registros de hábitos que pertenecen al usuario actual.
        return CompletionRecord.objects.filter(habit__user=self.request.user)
