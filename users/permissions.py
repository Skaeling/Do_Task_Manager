from rest_framework import permissions


class IsUser(permissions.BasePermission):
    message = "Viewing of this profile is not allowed"

    def has_object_permission(self, request, view, obj):
        return obj == request.user
