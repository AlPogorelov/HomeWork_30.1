from rest_framework.permissions import BasePermission


class IsOwnerOrModer(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь модератором или владельцем объекта
        return request.user.groups.filter(name='Moder').exists() or obj.owner == request.user


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        return obj.owner == request.user


class NotStaff(BasePermission):
    def has_permission(self, request, view):
        # Запрещаем доступ для staff-пользователей
        return not request.user.is_staff
