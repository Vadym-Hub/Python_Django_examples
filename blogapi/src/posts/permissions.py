"""Создаем свой класс разрешений переопределив метод has_object_permission"""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Только автор определенного сообщения в блоге может редактировать или
    удалять его; в противном случае сообщение в блоге должно быть только для чтения.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of a post
        return obj.author == request.user
