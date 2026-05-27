from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from habits.models import Habit, HabitLog, Streak
from google import genai


@login_required
def ai_analysis(request):
    user = request.user
    today = timezone.now().date()
    week_start = today - timezone.timedelta(days=7)
    habits = Habit.objects.filter(user=user, is_active=True)
    ai_response = None
    if request.method == 'POST':
        habits_info = []
        for habit in habits:
            logs = HabitLog.objects.filter(habit=habit, date__gte=week_start, completed=True).count()
            streak = Streak.objects.filter(habit=habit).first()
            habits_info.append(f"- {habit.name}: виконано {logs}/7 днів, streak: {streak.current_streak if streak else 0} днів")
        if habits_info:
            prompt = f"Ти AI-коуч. Проаналізуй звички українською: {', '.join(habits_info)}. Дай оцінку, 3 поради і мотивацію."
            try:
                client = genai.Client(api_key='AIzaSyBsbEoFaTbPKJsapuKxmyMCDOZIiUOnMLw')
                response = client.models.generate_content(model='gemini-2.0-flash-lite', contents=prompt)
                ai_response = response.text
            except Exception as e:
                ai_response = f"⚠️ AI тимчасово недоступний (перевищено ліміт запитів). Спробуй через кілька хвилин.\n\nТвоя статистика:\n" + "\n".join(habits_info)
        else:
            ai_response = "У тебе ще немає звичок для аналізу!"
    return render(request, 'ai_insight/ai_analysis.html', {'habits': habits, 'ai_response': ai_response})