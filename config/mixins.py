"""Модуль описывающий примеси с различным функционалом"""
import logging


class LoggerMixin:
    """Примесь для инициализации логера в классе"""
    logger = logging.getLogger('base')
