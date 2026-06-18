from rest_framework import serializers

from .models import Application
from jobs.models import Job


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.ReadOnlyField(
        source='applicant.username'
    )

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'applicant',
            'resume',
            'cover_letter',
            'status',
            'applied_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'applicant',
            'status',
            'applied_at',
            'updated_at',
        ]

    def validate_job(self, job):

        if not job.is_active:
            raise serializers.ValidationError(
                "This job is no longer accepting applications."
            )

        return job

    def validate(self, attrs):

        request = self.context['request']
        job = attrs.get('job')

        if Application.objects.filter(
            job=job,
            applicant=request.user
        ).exists():
            raise serializers.ValidationError(
                "You have already applied for this job."
            )

        return attrs

    def create(self, validated_data):

        validated_data['applicant'] = (
            self.context['request'].user
        )

        return super().create(validated_data)