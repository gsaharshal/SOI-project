from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import UserRole


class IsJobSeekerOrRecruiter(BasePermission):
    """
    Job Seekers:
        Can create applications.

    Recruiters:
        Can view applications.

    Admin:
        Full access.
    """

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.role == UserRole.ADMIN:
            return True

        if request.method in SAFE_METHODS:
            return True

        return request.user.role == UserRole.JOB_SEEKER