from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    # Allows access only to the owner of a Note.

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
