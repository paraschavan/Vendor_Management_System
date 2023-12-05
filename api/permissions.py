from rest_framework import permissions
from main.models import Vendor


class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user == None:
            return False
        vendor = Vendor.objects.filter(user=request.user)
        return vendor.exists()
