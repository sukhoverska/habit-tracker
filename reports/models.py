from django.db import models
from django.conf import settings


class WeeklyReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='weekly_reports'
    )
    week_start = models.DateField()
    week_end = models.DateField()
    total_habits = models.PositiveIntegerField(default=0)
    completed_count = models.PositiveIntegerField(default=0)
    completion_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    ai_summary = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'week_start')
        ordering = ['-week_start']

    def __str__(self):
        return f'{self.user.username} — {self.week_start}'