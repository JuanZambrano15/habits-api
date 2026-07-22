import pytest
from rest_framework.test import APIClient
from rest_framework import status
from apps.habits.factories import UserFactory, HabitFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    # force_authenticate: atajo de DRF para tests, evita tener que hacer
    # login real y manejar el token JWT en cada test — nos interesa probar
    # la lógica de la vista, no repetir la prueba de JWT que ya hicimos en Fase 3.
    return api_client, user


def test_unauthenticated_user_cannot_list_habits(api_client):
    response = api_client.get("/api/habits/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_user_can_create_habit(authenticated_client):
    client, user = authenticated_client
    response = client.post("/api/habits/", {
        "name": "Leer 20 minutos",
        "description": "",
        "scheduled_days": [0, 2, 4],
    }, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Leer 20 minutos"


def test_user_only_sees_own_habits(authenticated_client):
    client, user = authenticated_client
    HabitFactory(user=user)             # habito del usuario autenticado
    HabitFactory()                        # habito de OTRO usuario (SubFactory crea uno nuevo)

    response = client.get("/api/habits/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # solo ve el suyo, no el del otro usuario


def test_user_cannot_assign_habit_to_another_user(authenticated_client):
    client, user = authenticated_client
    response = client.post("/api/habits/", {
        "name": "Intento sospechoso",
        "user": 9999,  # aunque lo mande, no deberia tener efecto (ver Fase 2)
        "scheduled_days": [],
    }, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    from apps.habits.models import Habit
    created = Habit.objects.get(name="Intento sospechoso")
    assert created.user == user  # se asigno al usuario autenticado, no al id 9999