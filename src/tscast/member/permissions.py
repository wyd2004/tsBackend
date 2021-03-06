from rest_framework import permissions
class OnlyMemberAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return type(request.user) is Member

    def has_permission(self, request, view):
        return type(request.user) is Member
