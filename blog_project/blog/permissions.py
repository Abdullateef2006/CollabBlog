from rest_framework.permissions import BasePermission


class IsAuthorOrContributor(BasePermission):
    """
    Custom permission: Only the author or contributors can edit the post.
    """
    def has_object_permission(self, request, view, obj):
        # Allow editing only if the user is the author or a contributor
        return request.user == obj.author or request.user in obj.contributors.all()
