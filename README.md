# 📬 Mailer — Django REST рассылка

Простое приложение на Django REST Framework: вводишь email → приходит письмо.

---

## Требования

- Python 3.10+
- Git

---

## Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Chochopay/mailer.git
cd mailer

# 2. Создать виртуальное окружение
python -m venv .venv

# 3. Активировать
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS

# 4. Установить зависимости
pip install -r requirements.txt

# 5. Применить миграции
python manage.py migrate
```

---

## Настройка отправки писем (Gmail)

> Без этого шага письма будут выводиться только в консоль — реально не отправляться.

### Шаг 1 — Создай пароль приложения Gmail

1. Включи **двухфакторную аутентификацию**: https://myaccount.google.com/security
2. Перейди: **Google Аккаунт → Безопасность → Пароли приложений**
3. Создай пароль — получишь 16 символов вида `xxxx xxxx xxxx xxxx`

### Шаг 2 — Создай файл `.env`

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Открой `.env` и заполни своими данными:

```env
DEFAULT_FROM_EMAIL=your@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_USE_TLS=true
```

### Шаг 3 — Проверь, что всё работает

```bash
python manage.py send_test_email recipient@example.com
```

Если письмо пришло — всё настроено правильно. ✅

---

## Запуск сервера

```bash
python manage.py runserver
```

Открой браузер: **http://127.0.0.1:8000/**

Введи email в форму → нажми «Отправить» → письмо придёт на почту.

---

## Тесты

```bash
python manage.py test broadcast
```

Должно пройти **6/6 тестов**.

---

## Структура проекта

```
mailer/
├── broadcast/
│   ├── management/
│   │   └── commands/
│   │       └── send_test_email.py  # команда для проверки Gmail
│   ├── content.py      # тема и текст письма (редактируй здесь)
│   ├── serializers.py  # валидация email
│   ├── services.py     # DNS-проверка домена + отправка
│   ├── views.py        # API + страница
│   └── urls.py
├── config/
│   └── settings.py     # SMTP-конфиг через .env
├── templates/
│   └── index.html      # форма с тёмным дизайном
├── .env.example        # шаблон настроек (скопируй в .env)
└── requirements.txt
```

---

## Изменить текст письма

Открой [`broadcast/content.py`](broadcast/content.py) и замени `SUBJECT` и `BODY`.
