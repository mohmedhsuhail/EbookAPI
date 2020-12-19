from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from ebooks.models import Review

class IsAdminUserOrReadOnly(permissions.IsAdminUser):

	def has_permission(self,request,view):
		isadmin = super().has_permission(request,view)
		return isadmin or request.method in permissions.SAFE_METHODS

class IsReviewerOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.review_author==request.user  