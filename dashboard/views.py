from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserRole
from jobs.models import Job
from applications.models import (
    Application,
    ApplicationStatus
)

from .serializers import (
    RecruiterDashboardSerializer,
    JobSeekerDashboardSerializer
)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.role == UserRole.RECRUITER:

            jobs = Job.objects.filter(
                recruiter=user
            )

            total_jobs = jobs.count()

            active_jobs = jobs.filter(
                is_active=True
            ).count()

            inactive_jobs = jobs.filter(
                is_active=False
            ).count()

            total_applications = Application.objects.filter(
                job__recruiter=user
            ).count()

            data = {
                "total_jobs": total_jobs,
                "active_jobs": active_jobs,
                "inactive_jobs": inactive_jobs,
                "total_applications": total_applications,
            }

            serializer = RecruiterDashboardSerializer(data)

            return Response(serializer.data)

        if user.role == UserRole.JOB_SEEKER:

            applications = Application.objects.filter(
                applicant=user
            )

            data = {
                "total_applications":
                    applications.count(),

                "applied":
                    applications.filter(
                        status=ApplicationStatus.APPLIED
                    ).count(),

                "reviewed":
                    applications.filter(
                        status=ApplicationStatus.REVIEWED
                    ).count(),

                "shortlisted":
                    applications.filter(
                        status=ApplicationStatus.SHORTLISTED
                    ).count(),

                "rejected":
                    applications.filter(
                        status=ApplicationStatus.REJECTED
                    ).count(),

                "hired":
                    applications.filter(
                        status=ApplicationStatus.HIRED
                    ).count(),
            }

            serializer = JobSeekerDashboardSerializer(data)

            return Response(serializer.data)

        return Response({
            "message": "Dashboard unavailable."
        })