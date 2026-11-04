import dns.exception
import dns.resolver
from django.conf import settings
from django.core.mail import EmailMessage, mailers

from .content import BODY, SUBJECT

_LOOKUP_FAILURES = (
    dns.resolver.NoNameservers,
    dns.exception.Timeout,
)


class EmailCheckError(Exception):
    """DNS lookup failed, so existence is unknown."""


def domain_accepts_mail(email: str) -> bool:
    domain = email.rsplit("@", 1)[1].strip().rstrip(".").lower()
    try:
        domain = domain.encode("idna").decode("ascii")
    except UnicodeError:
        return False

    resolver = dns.resolver.Resolver()
    resolver.lifetime = 5
    try:
        answers = list(resolver.resolve(domain, "MX"))
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.NoAnswer:
        return _has_address(resolver, domain)
    except _LOOKUP_FAILURES as exc:
        raise EmailCheckError from exc

    exchanges = [str(answer.exchange).rstrip(".") for answer in answers]
    return any(exchanges)


def _has_address(resolver, domain: str) -> bool:
    for record_type in ("A", "AAAA"):
        try:
            resolver.resolve(domain, record_type)
            return True
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.NXDOMAIN:
            return False
        except _LOOKUP_FAILURES as exc:
            raise EmailCheckError from exc
    return False


def send_mailing(recipient: str) -> None:
    message = EmailMessage(
        subject=SUBJECT,
        body=BODY,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    mailers.default.send_messages([message])
