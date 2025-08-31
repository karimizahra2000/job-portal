from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobSeekerProfile, EmployerProfile, Job, JobApplication


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


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'status', 'is_published', 'created_at')
    list_filter = ('status', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'employer__username')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_jobs', 'reject_jobs', 'publish_jobs']

    def approve_jobs(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} job(s) approved.")
    approve_jobs.short_description = "Approve selected jobs"

    def reject_jobs(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} job(s) rejected.")
    reject_jobs.short_description = "Reject selected jobs"

    def publish_jobs(self, request, queryset):
        # Only allow publishing approved jobs
        updated = 0
        for job in queryset:
            if job.status == 'approved':
                job.is_published = True
                job.save()
                updated += 1
        self.message_user(request, f"{updated} job(s) published.")
    publish_jobs.short_description = "Publish selected jobs"


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "applicant", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("job__title", "applicant__username", "cover_letter")
    autocomplete_fields = ("job", "applicant")