"""Модуль описывающий модели базы данных приложения"""
from django.db import models


class LogData(models.Model):
    """Модель описывающая формат таблицы БД для хранения и обработки информации о логах"""
    time = models.DateTimeField(verbose_name='time')
    remote_ip = models.GenericIPAddressField(verbose_name='IP Address')
    method = models.CharField(max_length=32, verbose_name='method')
    url = models.CharField(max_length=1024, verbose_name='url')
    response = models.PositiveSmallIntegerField(verbose_name='response')
    bytes = models.PositiveBigIntegerField(verbose_name='bytes')
    remote_user = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name='remote user'
    )
    referrer = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name='referrer'
    )
    agent = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name='agent'
    )

    class Meta:
        """Класс, определяющий некоторые параметры модели"""
        ordering = ['pk']
        verbose_name = 'log'
        verbose_name_plural = 'logs'
        unique_together = ['time', 'remote_ip', 'method', 'url']

    def __str__(self):
        return (f'id: {self.pk} | {self.time.strftime("%d.%m.%Y %H:%M:%S")} '
                f'IP: {self.remote_ip} {self.method} {self.url}')
