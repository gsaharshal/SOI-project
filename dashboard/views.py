from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from jobs.models import Job
from applications.models import Application

from .serializers import (
    RecruiterDashboardSerializer,
    JobSeekerDashboardSerializer
)


class DashboardViewSet(ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def recruiter(self, request):

        user = request.user

        jobs = Job.objects.filter(recruiter=user)

        total_jobs = jobs.count()

        active_jobs = jobs.filter(status="ACTIVE").count()

        inactive_jobs = jobs.exclude(
            status="ACTIVE"
        ).count()

        total_applications = Application.objects.filter(
            job__recruiter=user
        ).count()

        serializer = RecruiterDashboardSerializer({
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "inactive_jobs": inactive_jobs,
            "total_applications": total_applications
        })

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def jobseeker(self, request):

        user = request.user

        applications = Application.objects.filter(
            applicant=user
        )

        serializer = JobSeekerDashboardSerializer({
            "total_applications": applications.count(),
            "applied": applications.filter(
                status="APPLIED"
            ).count(),
            "reviewed": applications.filter(
                status="REVIEWED"
            ).count(),
            "shortlisted": applications.filter(
                status="SHORTLISTED"
            ).count(),
            "rejected": applications.filter(
                status="REJECTED"
            ).count(),
        })

        return Response(serializer.data)