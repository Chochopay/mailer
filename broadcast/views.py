import logging
from smtplib import SMTPException

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .serializers import SendMailingSerializer
from .services import EmailCheckError, domain_accepts_mail, send_mailing

logger = logging.getLogger(__name__)


class SendRateThrottle(AnonRateThrottle):
    rate = "5/min"


@method_decorator(ensure_csrf_cookie, name="dispatch")
class HomeView(TemplateView):
    template_name = "index.html"


class SendMailingView(APIView):
    throttle_classes = [SendRateThrottle]

    def post(self, request):
        serializer = SendMailingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            exists = domain_accepts_mail(email)
        except EmailCheckError:
            logger.warning("Email check failed for %s", email, exc_info=True)
            return Response(
                {"email": ["Не удалось проверить email. Попробуйте ещё раз."]},
                status=503,
            )

        if not exists:
            raise ValidationError({"email": ["Такой email не существует."]})

        try:
            send_mailing(email)
        except (OSError, SMTPException):
            logger.exception("Failed to send mailing to %s", email)
            return Response(
                {"detail": "Не удалось отправить письмо."},
                status=502,
            )

        return Response({"detail": "Письмо отправлено."})
