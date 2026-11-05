"""
Management command для проверки отправки писем.

Использование:
    python manage.py send_test_email recipient@example.com

Отправляет тестовое письмо через настроенный backend (SMTP или консоль).
Позволяет убедиться, что Gmail / SMTP работают без запуска сервера.
"""

from django.core.management.base import BaseCommand, CommandError

from broadcast.services import send_mailing


class Command(BaseCommand):
    help = "Отправить тестовое письмо на указанный адрес"

    def add_arguments(self, parser):
        parser.add_argument(
            "email",
            type=str,
            help="Email-адрес получателя тестового письма",
        )

    def handle(self, *args, **options):
        recipient = options["email"]
        self.stdout.write(f"Отправляю письмо на {recipient}...")
        try:
            send_mailing(recipient)
        except Exception as exc:
            raise CommandError(f"Не удалось отправить письмо: {exc}") from exc
        self.stdout.write(self.style.SUCCESS(f"✓ Письмо успешно отправлено на {recipient}"))
