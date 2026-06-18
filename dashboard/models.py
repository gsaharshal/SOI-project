from django.db import models
from django.conf import settings
from jobs.models import Job
from applications.models import Application


# ⚠️ Dashboard is NOT stored in DB in most cases
# It is computed from Job + Application tables

class DashboardSnapshot(models.Model):
    """
    OPTIONAL:
    Use this only if you want to store historical analytics.
    Otherwise, you can ignore this model completely.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dashboard_snapshots"
    )

    total_jobs = models.IntegerField(default=0)
    active_jobs = models.IntegerField(default=0)
    inactive_jobs = models.IntegerField(default=0)

    total_applications = models.IntegerField(default=0)

    applied = models.IntegerField(default=0)
    reviewed = models.IntegerField(default=0)
    shortlisted = models.IntegerField(default=0)
    rejected = models.IntegerField(default=0)
    hired = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Snapshot - {self.user.username} - {self.created_at.date()}"