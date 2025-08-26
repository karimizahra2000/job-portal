from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobSeekerProfile, EmployerProfile


class JobSeekerProfileInline(admin.StackedInline):
    model = JobSeekerProfile
    can_delete = False


class EmployerProfileInline(admin.StackedInline):
    model = EmployerProfile
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "email", "is_seeker", "is_employer", "is_verified", "is_staff")
    list_filter = ("is_seeker", "is_employer", "is_verified", "is_staff")
    search_fields = ("username", "email")
    inlines = [JobSeekerProfileInline, EmployerProfileInline]


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ("user__username", "user__email")


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "company_name")
    search_fields = ("user__username", "user__email", "company_name")
