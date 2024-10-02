"""Модуль для реализации сериализаторов приложения"""
from rest_framework import serializers
from .models import LogData


class LogsSerializer(serializers.ModelSerializer):
    """Класс описывающий сериализатор данных модели LogData"""

    class Meta:
        """Класс, определяющий некоторые параметры сериализатора"""
        model = LogData
        fields = (
            'time',
            'remote_ip',
            'method',
            'url',
            'response',
            'bytes',
            'remote_user',
            'referrer',
            'agent',
        )
