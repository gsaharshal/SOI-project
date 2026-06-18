from rest_framework import serializers


class RecruiterDashboardSerializer(serializers.Serializer):
    total_jobs = serializers.IntegerField()
    active_jobs = serializers.IntegerField()
    inactive_jobs = serializers.IntegerField()
    total_applications = serializers.IntegerField()


class JobSeekerDashboardSerializer(serializers.Serializer):
    total_applications = serializers.IntegerField()
    applied = serializers.IntegerField()
    reviewed = serializers.IntegerField()
    shortlisted = serializers.IntegerField()
    rejected = serializers.IntegerField()
    hired = serializers.IntegerField()