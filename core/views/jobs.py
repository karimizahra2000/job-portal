from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.serializers import JobSerializer
from core.permissions import IsEmployer, IsOwnerOrAdmin
from core.utils.pagination import CachedPagination
from core.repositories.jobs import JobRepository


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer, IsOwnerOrAdmin]
    pagination_class = CachedPagination

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get("status")
        return JobRepository.get_all(user, status_filter)

    def perform_create(self, serializer):
        JobRepository.create(employer=self.request.user, **serializer.validated_data)

    def perform_update(self, serializer):
        job = self.get_object()
        JobRepository.update(job, **serializer.validated_data)

    def perform_destroy(self, instance):
        JobRepository.delete(instance)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        job = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        JobRepository.approve(job)
        return Response({"status": "approved"})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        job = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        reason = request.data.get("reason", "")
        JobRepository.reject(job, reason)
        return Response({"status": "rejected", "reason": reason})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        job = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        try:
            JobRepository.publish(job)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "published"})
