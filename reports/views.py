from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from habits.models import Habit, HabitLog
import json


@login_required
def reports(request):
    user = request.user
    today = timezone.now().date()
    
    # Останні 365 днів для heatmap
    start_date = today - timezone.timedelta(days=365)
    logs = HabitLog.objects.filter(
        habit__user=user,
        date__gte=start_date,
        completed=True
    ).values('date')
    
    # Підраховуємо кількість виконаних звичок по днях
    heatmap_data = {}
    for log in logs:
        date_str = log['date'].strftime('%Y-%m-%d')
        heatmap_data[date_str] = heatmap_data.get(date_str, 0) + 1
    
    # Тижневий звіт
    week_start = today - timezone.timedelta(days=today.weekday())
    week_logs = HabitLog.objects.filter(
        habit__user=user,
        date__gte=week_start,
        completed=True
    ).count()
    total_habits = Habit.objects.filter(user=user, is_active=True).count()
    week_total = total_habits * 7
    week_rate = round((week_logs / week_total * 100) if week_total > 0 else 0)
    
    # Місячний звіт
    month_start = today.replace(day=1)
    month_logs = HabitLog.objects.filter(
        habit__user=user,
        date__gte=month_start,
        completed=True
    ).count()
    days_passed = today.day
    month_total = total_habits * days_passed
    month_rate = round((month_logs / month_total * 100) if month_total > 0 else 0)
    
    return render(request, 'reports/reports.html', {
        'heatmap_data': json.dumps(heatmap_data),
        'week_logs': week_logs,
        'week_rate': week_rate,
        'month_logs': month_logs,
        'month_rate': month_rate,
        'total_habits': total_habits,
    })