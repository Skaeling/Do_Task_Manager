from rest_framework import permissions


class IsUser(permissions.BasePermission):
    message = "Viewing of this profile is not allowed"

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsSupervisor(permissions.BasePermission):
    """Разрешение, позволяющее доступ только юзерам, имеющим должность супервайзера в positions"""
    message = "You're not supervisor"

    def has_permission(self, request, view):
        return hasattr(request.user, 'positions') and request.user.positions.filter(is_supervisor=True).exists()


class IsExecutor(permissions.BasePermission):
    message = "Viewing of this task is not allowed"

    def has_object_permission(self, request, view, obj):
        if obj.executor is not None:
            return request.user.positions.filter(id=obj.executor.id).exists()
        return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
