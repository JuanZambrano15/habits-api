from django.urls import path
from .views import HabitAnalyticsView

urlpatterns = [
    path("summary/", HabitAnalyticsView.as_view(), name="analytics-summary"),
]