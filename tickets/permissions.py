from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == request.user.Role.ADMIN
    

class CanAccessTicket(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == user.Role.ADMIN:
            return True
        if user.role == user.Role.EMPLOYEE:
            return obj.employee == user
        if user.role == user.Role.IT_STAFF:
            return obj.assigned_to == user

        return False