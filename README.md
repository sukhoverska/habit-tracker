# 🎯 HabitTracker

Трекер звичок і продуктивності на Django. Створення звичок, щоденне відмічання, серії днів (streak), тижневі/місячні звіти, heatmap активності та AI аналіз.

## ✨ Функціонал

- 📝 Створення, редагування та видалення звичок
- ✅ Щоденне відмічання виконання
- 🔥 Streak система — серії днів
- 📊 Тижневі та місячні звіти з графіками
- 🗓 Heatmap активності за рік
- 🤖 AI аналіз звичок через Google Gemini
- 🔐 Реєстрація та автентифікація користувачів

## 🛠 Стек технологій

- **Backend:** Django 6, PostgreSQL, Gunicorn
- **Frontend:** HTML, CSS, JavaScript
- **AI:** Google Gemini API
- **DevOps:** Docker, Nginx
- **Тести:** Django TestCase (9 тестів)

## 🚀 Як запустити локально

**1. Клонуй репозиторій**

```bash
git clone https://github.com/sukhoverska/habit-tracker.git
cd habit-tracker
```

**2. Створи віртуальне середовище**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Встанови залежності**

```bash
pip install -r requirements.txt
```

**4. Налаштуй змінні середовища**

Скопіюй `.env.example` у `.env` і заповни:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=habit_tracker
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
GEMINI_API_KEY=your-gemini-api-key
```

**5. Створи базу даних PostgreSQL**

```bash
psql -U postgres -c "CREATE DATABASE habit_tracker;"
```

**6. Виконай міграції**

```bash
python manage.py migrate
```

**7. Створи суперкористувача**

```bash
python manage.py createsuperuser
```

**8. Запусти сервер**

```bash
python manage.py runserver
```

Відкрий браузер: **http://127.0.0.1:8000**

## 🐳 Запуск через Docker

**1. Клонуй репозиторій і налаштуй .env**

```bash
git clone https://github.com/sukhoverska/habit-tracker.git
cd habit-tracker
cp .env.example .env
```

**2. Запусти через Docker Compose**

```bash
docker-compose up --build
```

Відкрий браузер: **http://localhost**

## 🧪 Запуск тестів

```bash
python manage.py test habits
```

Результат: 9 тестів, всі проходять ✅

## 📁 Структура проєкту
