from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    recruiter = serializers.ReadOnlyField(source='recruiter.username')

    class Meta:
        model = Job
        fields = [
            'id',
            'recruiter',
            'title',
            'description',
            'location',
            'employment_type',
            'experience_level',
            'skills',
            'vacancy_count',
            'salary_min',
            'salary_max',
            'application_deadline',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'recruiter',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')

        if (
            salary_min is not None
            and salary_max is not None
            and salary_min > salary_max
        ):
            raise serializers.ValidationError(
                "Minimum salary cannot be greater than maximum salary."
            )

        return attrs

    def create(self, validated_data):
        validated_data['recruiter'] = self.context[
            'request'
        ].user

        return super().create(validated_data)