from abc import ABC
from typing import ClassVar, List, TypeVar

from django.db.models import Model

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

ModelType = TypeVar("ModelType", bound=Model)


class BaseAPIViewSet(ABC, ModelViewSet[ModelType]):
    """
    A base ViewSet that includes common filter backends and default ordering.
    """

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    ordering_fields: ClassVar[List[str]] = ["id"]
