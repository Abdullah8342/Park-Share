'''
    Permissions.py
'''

from rest_framework import permissions


class IsDriverOnly(permissions.BasePermission):
    '''
        Is Driver Only
    '''
    def has_object_permission(self, request, view, obj):
        print("Is Driver Only has object permission")
        return request.user and request.user.is_authenticated and request.user == obj.driver
