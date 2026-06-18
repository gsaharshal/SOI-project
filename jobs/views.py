from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Job
from .serializers import JobSerializer
from .permissions import IsRecruiterAndOwnerOrReadOnly


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [
        IsAuthenticated,
        IsRecruiterAndOwnerOrReadOnly
    ]

    def get_queryset(self):
        queryset = Job.objects.all()

        location = self.request.query_params.get('location')
        employment_type = self.request.query_params.get(
            'employment_type'
        )
        is_active = self.request.query_params.get(
            'is_active'
        )

        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        if employment_type:
            queryset = queryset.filter(
                employment_type=employment_type
            )

        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(
                    is_active=True
                )
            elif is_active.lower() == 'false':
                queryset = queryset.filter(
                    is_active=False
                )

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            recruiter=self.request.user
        )