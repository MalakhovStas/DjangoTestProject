"""Модуль настройки Django админки приложения"""
from django.contrib import admin
from .models import LogData


@admin.register(LogData)
class LogDataAdmin(admin.ModelAdmin):
    """Регистрация модели LogData в Django admin"""
    search_fields = ['pk', 'time', 'remote_ip', 'method', 'url', 'response']
    list_filter = ['time', 'remote_ip', 'method', 'url', 'response']
