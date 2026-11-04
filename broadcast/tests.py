from unittest.mock import Mock, patch

import dns.resolver
from django.core import mail
from django.test import SimpleTestCase, override_settings
from rest_framework.test import APITestCase

from broadcast.services import domain_accepts_mail

LOCMEM = {
    "default": {
        "BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    }
}


class DomainAcceptsMailTests(SimpleTestCase):
    @patch("broadcast.services.dns.resolver.Resolver")
    def test_mx_record_counts_as_existing(self, resolver_cls):
        record = Mock()
        record.exchange = "mx.example.com."
        resolver_cls.return_value.resolve.return_value = [record]

        self.assertTrue(domain_accepts_mail("person@example.com"))

    @patch("broadcast.services.dns.resolver.Resolver")
    def test_null_mx_does_not_accept_mail(self, resolver_cls):
        record = Mock()
        record.exchange = "."
        resolver_cls.return_value.resolve.return_value = [record]

        self.assertFalse(domain_accepts_mail("person@example.com"))

    @patch("broadcast.services.dns.resolver.Resolver")
    def test_missing_domain(self, resolver_cls):
        resolver_cls.return_value.resolve.side_effect = dns.resolver.NXDOMAIN()

        self.assertFalse(domain_accepts_mail("person@missing.test"))


@override_settings(MAILERS=LOCMEM)
class SendMailingApiTests(APITestCase):
    def test_rejects_invalid_format(self):
        response = self.client.post(
            "/api/send/",
            {"email": "not-an-email"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    @patch("broadcast.views.domain_accepts_mail", return_value=False)
    def test_rejects_domain_without_mail(self, _exists):
        response = self.client.post(
            "/api/send/",
            {"email": "person@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("не существует", response.json()["email"][0])

    @patch("broadcast.views.domain_accepts_mail", return_value=True)
    def test_sends_prepared_text(self, _exists):
        response = self.client.post(
            "/api/send/",
            {"email": "person@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["person@example.com"])
        self.assertEqual(mail.outbox[0].subject, "Рассылка")
