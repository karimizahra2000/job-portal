from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import JobApplication
from core.serializers import JobApplicationSerializer
from core.permissions import IsOwnerOrAdmin, IsEmployer
from rest_framework.decorators import action


class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_employer:

            return JobApplication.objects.filter(job__employer=user)
        else:

            return JobApplication.objects.filter(applicant=user)

    def perform_create(self, serializer):

        serializer.save(applicant=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        application = self.get_object()
        if not request.user.is_employer:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        application.status = 'accepted'
        application.save()
        return Response({"status": "accepted"})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        application = self.get_object()
        if not request.user.is_employer:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        application.status = 'rejected'
        application.save()
        return Response({"status": "rejected"})
