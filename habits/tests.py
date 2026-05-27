from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from .models import Habit, HabitLog, Streak, Category

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            name='Читати 30 хв',
            frequency='daily'
        )

    def test_habit_created(self):
        self.assertEqual(self.habit.name, 'Читати 30 хв')
        self.assertEqual(self.habit.user, self.user)
        self.assertTrue(self.habit.is_active)

    def test_habit_str(self):
        self.assertIn('Читати 30 хв', str(self.habit))

    def test_streak_created_with_habit(self):
        Streak.objects.create(habit=self.habit)
        streak = Streak.objects.get(habit=self.habit)
        self.assertEqual(streak.current_streak, 0)


class HabitLogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            name='Спорт',
            frequency='daily'
        )

    def test_log_created(self):
        today = timezone.now().date()
        log = HabitLog.objects.create(
            habit=self.habit,
            date=today,
            completed=True
        )
        self.assertTrue(log.completed)
        self.assertEqual(log.date, today)

    def test_unique_log_per_day(self):
        today = timezone.now().date()
        HabitLog.objects.create(habit=self.habit, date=today, completed=True)
        with self.assertRaises(Exception):
            HabitLog.objects.create(habit=self.habit, date=today, completed=True)


class HabitViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser3',
            password='testpass123'
        )
        self.client.login(username='testuser3', password='testpass123')
        self.habit = Habit.objects.create(
            user=self.user,
            name='Медитація',
            frequency='daily'
        )
        Streak.objects.create(habit=self.habit)

    def test_habit_list_view(self):
        response = self.client.get(reverse('habit_list'))
        self.assertEqual(response.status_code, 200)

    def test_habit_create_view(self):
        response = self.client.get(reverse('habit_create'))
        self.assertEqual(response.status_code, 200)

    def test_habit_complete_view(self):
        response = self.client.get(
            reverse('habit_complete', args=[self.habit.id])
        )
        self.assertEqual(response.status_code, 302)
        log = HabitLog.objects.filter(
            habit=self.habit,
            date=timezone.now().date()
        ).first()
        self.assertIsNotNone(log)
        self.assertTrue(log.completed)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('habit_list'))
        self.assertEqual(response.status_code, 302)