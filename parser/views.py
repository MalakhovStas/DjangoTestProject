"""Модуль для реализации отображений приложения"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework.backends import DjangoFilterBackend  # type: ignore
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import LogData
from .serializers import LogsSerializer


class LogsDataViewSet(ModelViewSet):
    """Набор представлений для осуществления CRUD операций с моделью LogData"""
    queryset = LogData.objects.all()
    serializer_class = LogsSerializer
    filter_backends = (
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    )
    search_fields = ('time', 'remote_ip', 'method', 'url', 'response')
    filterset_fields = ('time', 'remote_ip', 'method', 'url', 'response')
    ordering_fields = ('time', 'remote_ip', 'method', 'url', 'response')

    @method_decorator(cache_page(0.1))
    def list(self, *args, **kwargs):
        """Метод получения списка экземпляров модели LogData"""
        return super().list(*args, **kwargs)
