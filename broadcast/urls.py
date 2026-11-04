from django.urls import path

from .views import HomeView, SendMailingView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("api/send/", SendMailingView.as_view(), name="send-mailing"),
]
