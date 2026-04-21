"""
permissions.py
"""

from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from .models import Organization


class IsOwner(BasePermission):
    """
    Only Owner
    """

    def has_permission(self, request, view):
        print("IsOwner has_permission")
        return (
            request.user and request.user.is_authenticated and request.user.roll == "PO"
        )

    def has_object_permission(self, request, view, obj):
        print("IsOwner has_object_permission")
        return bool(request.user == obj.owner and request.user.roll == "PO")


class IsOwnerOrReadOnly(BasePermission):
    """
    Only Owner Can Perform Action Other Can See
    """

    def has_permission(self, request, view):
        print("IsOwnerOrReadOnly has_permission")
        return (
            request.user
            and request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.roll == "PO"
        )

    def has_object_permission(self, request, view, obj):
        print("IsOwnerOrReadOnly has_object_permission")
        return bool(
            request.method in SAFE_METHODS
            or request.user == obj.owner
            and request.user.roll == "PO"
        )


class IsSpotOwnerOrReadOnly(BasePermission):
    """
    Only Owner Can Perform Action Other Can See
    """

    def has_object_permission(self, request, view, obj):
        print("IsSpotOwnerOrReadOnly has_object_permission")
        # NEED: TO CHECK organization_owner = obj.organization.owner
        organization_object = get_object_or_404(Organization, id=obj.id)
        organization_owner = request.user == organization_object.owner
        return bool(
            request.method in SAFE_METHODS
            or request.user.roll == "PO"
            and organization_owner
        )
