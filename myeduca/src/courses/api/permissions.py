from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """Проверяем, является ли текущий пользователь слушателем курса"""
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()
