from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class NotAllowList(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True

    def has_permission(self, request, view):
        return True


class AuthenticatedUserCanPost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_anonymous():
            return False
        else:
            return True

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_anonymous():
            return False
        else:
            return True


class OnlyAuthenticatedUserPost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return False

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return False
        elif request.user.is_anonymous():
            return False
        else:
            return True
