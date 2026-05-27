from django.contrib import admin
from .models import Category, Habit, HabitLog, Streak

admin.site.register(Category)
admin.site.register(Habit)
admin.site.register(HabitLog)
admin.site.register(Streak)