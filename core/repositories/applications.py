from core.models import JobApplication
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet


class JobApplicationRepository:
    @staticmethod
    def get_all(user, status_filter: str | None = None) -> QuerySet:
        if getattr(user, "is_employer", False) or user.is_staff:
            qs = JobApplication.objects.filter(job__employer=user)
        else:
            qs = JobApplication.objects.filter(applicant=user)

        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs.order_by("-created_at")

    @staticmethod
    def get_by_id(app_id: int) -> JobApplication:
        return get_object_or_404(JobApplication, id=app_id)

    @staticmethod
    def get_by_job(user, job_id: int, status_filter: str | None = None) -> QuerySet:
        if not getattr(user, "is_employer", False):
            return JobApplication.objects.none()

        qs = JobApplication.objects.filter(job_id=job_id, job__employer=user)
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs.order_by("-created_at")

    @staticmethod
    def create(applicant, **kwargs) -> JobApplication:
        return JobApplication.objects.create(applicant=applicant, **kwargs)

    @staticmethod
    def update(application: JobApplication, **kwargs) -> JobApplication:
        for field, value in kwargs.items():
            setattr(application, field, value)
        application.save()
        return application

    @staticmethod
    def delete(application: JobApplication):
        application.delete()

    @staticmethod
    def accept(application: JobApplication):
        application.status = 'accepted'
        application.save()
        return application

    @staticmethod
    def reject(application: JobApplication):
        application.status = 'rejected'
        application.save()
        return application
