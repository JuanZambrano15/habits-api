from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, DayOfWeekViewSet, CompletionRecordViewSet

router = DefaultRouter()
router.register("habits", HabitViewSet, basename="habit")
router.register("days", DayOfWeekViewSet, basename="dayofweek")
router.register("completion-records", CompletionRecordViewSet, basename="completionrecord")

urlpatterns = router.urls