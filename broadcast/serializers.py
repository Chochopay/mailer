from rest_framework import serializers


class SendMailingSerializer(serializers.Serializer):
    email = serializers.EmailField()
