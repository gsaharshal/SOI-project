from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    RecruiterProfile,
    JobSeekerProfile
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active'
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active'
    )


admin.site.register(RecruiterProfile)
admin.site.register(JobSeekerProfile)