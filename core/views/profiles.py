from rest_framework import generics, permissions
from core.models import JobSeekerProfile, EmployerProfile
from core.serializers import JobSeekerProfileSerializer, EmployerProfileSerializer


class JobSeekerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return JobSeekerProfile.objects.get(user=self.request.user)


class EmployerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)
