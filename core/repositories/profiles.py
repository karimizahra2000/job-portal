from core.models import JobSeekerProfile, EmployerProfile
from django.shortcuts import get_object_or_404


class JobSeekerProfileRepository:
    @staticmethod
    def get_all():
        return JobSeekerProfile.objects.all()

    @staticmethod
    def get_by_id(profile_id: int) -> JobSeekerProfile:
        return get_object_or_404(JobSeekerProfile, id=profile_id)

    @staticmethod
    def get_by_user(user) -> JobSeekerProfile | None:
        return JobSeekerProfile.objects.filter(user=user).first()

    @staticmethod
    def create(user, **kwargs) -> JobSeekerProfile:
        return JobSeekerProfile.objects.create(user=user, **kwargs)

    @staticmethod
    def update(profile: JobSeekerProfile, **kwargs) -> JobSeekerProfile:
        for field, value in kwargs.items():
            setattr(profile, field, value)
        profile.save()
        return profile

    @staticmethod
    def delete(profile: JobSeekerProfile):
        profile.delete()


class EmployerProfileRepository:
    @staticmethod
    def get_all():
        return EmployerProfile.objects.all()

    @staticmethod
    def get_by_id(profile_id: int) -> EmployerProfile:
        return get_object_or_404(EmployerProfile, id=profile_id)

    @staticmethod
    def get_by_user(user) -> EmployerProfile | None:
        return EmployerProfile.objects.filter(user=user).first()

    @staticmethod
    def create(user, **kwargs) -> EmployerProfile:
        return EmployerProfile.objects.create(user=user, **kwargs)

    @staticmethod
    def update(profile: EmployerProfile, **kwargs) -> EmployerProfile:
        for field, value in kwargs.items():
            setattr(profile, field, value)
        profile.save()
        return profile

    @staticmethod
    def delete(profile: EmployerProfile):
        profile.delete()
