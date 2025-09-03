from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from core.serializers import JobSeekerProfileSerializer, EmployerProfileSerializer
from core.repositories.profiles import JobSeekerProfileRepository, EmployerProfileRepository


class JobSeekerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile = JobSeekerProfileRepository.get_by_user(self.request.user)
        if not profile:
            raise NotFound("Job seeker profile not found.")
        return profile


class EmployerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile = EmployerProfileRepository.get_by_user(self.request.user)
        if not profile:
            raise NotFound("Employer profile not found.")
        return profile
