from django.contrib import admin
from .models import DayOfWeek, Habit, CompletionRecord

admin.site.register(DayOfWeek)
admin.site.register(Habit)
admin.site.register(CompletionRecord)
