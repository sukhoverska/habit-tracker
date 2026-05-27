from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Habit, HabitLog, Streak
from .forms import HabitForm


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user, is_active=True)
    today = timezone.now().date()

    habits_data = []
    for habit in habits:
        log_today = HabitLog.objects.filter(habit=habit, date=today).first()
        streak = Streak.objects.filter(habit=habit).first()
        habits_data.append({
            'habit': habit,
            'completed_today': log_today.completed if log_today else False,
            'streak': streak.current_streak if streak else 0,
        })

    return render(request, 'habits/habit_list.html', {
        'habits_data': habits_data,
        'today': today,
    })


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            Streak.objects.create(habit=habit)
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {'form': form})


@login_required
def habit_complete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.now().date()

    log, created = HabitLog.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'completed': True}
    )

    if not created:
        log.completed = not log.completed
        log.save()

    streak, _ = Streak.objects.get_or_create(habit=habit)

    if log.completed:
        yesterday = today - timezone.timedelta(days=1)
        if streak.last_completed_date == yesterday:
            streak.current_streak += 1
        elif streak.last_completed_date != today:
            streak.current_streak = 1
        streak.last_completed_date = today
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
    streak.save()

    return redirect('habit_list')


@login_required
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        habit.is_active = False
        habit.archived_at = timezone.now()
        habit.save()
    return redirect('habit_list')


@login_required
def habit_edit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {'form': form, 'edit': True})