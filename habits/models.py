from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#4F46E5')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Щодня'),
        ('weekly', 'Щотижня'),
        ('custom', 'Власна'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='habits'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='daily'
    )
    target_days = models.JSONField(
        default=list,
        blank=True,
        help_text='Для custom: [0,1,2,3,4] — дні тижня (0=Пн)'
    )
    color = models.CharField(max_length=7, default='#4F46E5')
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.name}'


class HabitLog(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    date = models.DateField()
    completed = models.BooleanField(default=True)
    note = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('habit', 'date')
        ordering = ['-date']

    def __str__(self):
        status = '✓' if self.completed else '✗'
        return f'{status} {self.habit.name} — {self.date}'


class Streak(models.Model):
    habit = models.OneToOneField(
        Habit,
        on_delete=models.CASCADE,
        related_name='streak'
    )
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_completed_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.habit.name}: {self.current_streak} днів'