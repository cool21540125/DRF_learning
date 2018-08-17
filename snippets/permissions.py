"""
    Tutorial 4 : 權限
"""
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        只允許 物件擁有者 修改
    """
    def has_object_permission(self, request, view, obj):
        '''
            GET, HEAD, OPTIONS for all only
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
