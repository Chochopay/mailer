# 🚀 Запуск mailer на новом компьютере

## Требования
- Python 3.10+
- Git

---

## 1. Клонировать репозиторий

```bash
git clone https://github.com/Chochopay/mailer.git
cd mailer
```

---

## 2. Создать виртуальное окружение и установить зависимости

```bash
# Создать venv
python -m venv .venv

# Активировать (Windows)
.venv\Scripts\activate

# Активировать (Linux / macOS)
source .venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

---

## 3. Настроить переменные окружения

Скопируй `.env.example` в `.env` и заполни своими данными:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Открой `.env` и укажи настройки SMTP:

```env
DEFAULT_FROM_EMAIL=newsletter@yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=true
```

> [!NOTE]
> Если `.env` не создавать — письма будут просто выводиться в консоль (режим разработки). Удобно для тестирования без реального SMTP.

---

## 4. Применить миграции

```bash
python manage.py migrate
```

---

## 5. Запустить сервер

```bash
python manage.py runserver
```

Открой браузер: **http://127.0.0.1:8000/**

---

## 6. (Опционально) Запустить тесты

```bash
python manage.py test broadcast
```

Должно пройти **6/6 тестов**.

---

## Итоговая последовательность (кратко)

```bash
git clone https://github.com/Chochopay/mailer.git
cd mailer
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
copy .env.example .env        # заполнить .env своими данными
python manage.py migrate
python manage.py runserver
```
