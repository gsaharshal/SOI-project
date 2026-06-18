from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import UserRole


class IsRecruiterAndOwnerOrReadOnly(BasePermission):
    """
    Read:
        Any authenticated user.

    Create:
        Recruiters only.

    Update/Delete:
        Only the recruiter who created the job.
    """

def has_permission(self, request, view):

    print("USER:", request.user)
    print("ROLE:", getattr(request.user, "role", None))
    print("METHOD:", request.method)

    if request.method in SAFE_METHODS:
        return request.user and request.user.is_authenticated

    return (
        request.user.is_authenticated
        and request.user.role == UserRole.RECRUITER
    )

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.recruiter == request.user