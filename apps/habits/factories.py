import factory
from apps.accounts.models import User
from apps.habits.models import Habit, DayOfWeek, CompletionRecord


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@test.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    # PostGenerationMethodCall: llama a user.set_password("testpass123") DESPUÉS
    # de crear el objeto, para que quede hasheado igual que en producción,
    # en vez de guardar "testpass123" en texto plano en el campo password.


class HabitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Habit

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Habito {n}")
    is_active = True


class CompletionRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompletionRecord

    habit = factory.SubFactory(HabitFactory)
    status = "completed"