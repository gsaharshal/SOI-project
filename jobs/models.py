from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class EmploymentType(models.TextChoices):
    FULL_TIME = "FULL_TIME", "Full Time"
    PART_TIME = "PART_TIME", "Part Time"
    INTERNSHIP = "INTERNSHIP", "Internship"
    CONTRACT = "CONTRACT", "Contract"
    REMOTE = "REMOTE", "Remote"


class ExperienceLevel(models.TextChoices):
    FRESHER = "FRESHER", "Fresher"
    JUNIOR = "JUNIOR", "Junior"
    MID_LEVEL = "MID_LEVEL", "Mid Level"
    SENIOR = "SENIOR", "Senior"


class Job(models.Model):
    recruiter = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="jobs"
)

    title = models.CharField(max_length=255)

    description = models.TextField()

    location = models.CharField(max_length=255)

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices
    )

    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.FRESHER
    )

    skills = models.TextField(
        blank=True,
        help_text="Comma-separated skills"
    )

    vacancy_count = models.PositiveIntegerField(default=1)

    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    application_deadline = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        indexes = [
            models.Index(fields=["location"]),
            models.Index(fields=["employment_type"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]

    def clean(self):
        if (
            self.salary_min is not None
            and self.salary_max is not None
            and self.salary_min > self.salary_max
        ):
            raise ValidationError(
                "Minimum salary cannot be greater than maximum salary."
            )

    def __str__(self):
        return self.title