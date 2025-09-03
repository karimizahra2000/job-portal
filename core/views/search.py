# core/views/search.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from core.repositories.search import JobSearchRepository
from core.serializers import JobSerializer


class JobSearchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        query = request.query_params.get("q", "")
        status_filter = request.query_params.get("status")
        employer_filter = request.query_params.get("employer")

        results = JobSearchRepository.search_jobs(
            query=query,
            status=status_filter,
            employer=employer_filter
        )

        serializer = JobSerializer(results, many=True)
        return Response(serializer.data)
