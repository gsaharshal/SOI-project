from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserRole
from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsJobSeekerOrRecruiter


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [
        IsAuthenticated,
        IsJobSeekerOrRecruiter
    ]

    def get_queryset(self):
        user = self.request.user

        # Admin can see all applications
        if user.role == UserRole.ADMIN:
            return Application.objects.all()

        # Job Seeker can see own applications
        if user.role == UserRole.JOB_SEEKER:
            return Application.objects.filter(
                applicant=user
            )

        # Recruiter can see applications
        # for jobs they posted
        if user.role == UserRole.RECRUITER:
            return Application.objects.filter(
                job__recruiter=user
            )

        return Application.objects.none()

    def perform_create(self, serializer):
        serializer.save(
            applicant=self.request.user
        )