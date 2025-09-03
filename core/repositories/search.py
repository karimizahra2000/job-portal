# core/repositories/search.py
from elasticsearch_dsl import Q
from core.search_indexes import JobDocument


class JobSearchRepository:
    @staticmethod
    def search_jobs(query: str = "", status: str = None, employer: str = None):
        """
        Search jobs using ElasticSearch with optional filters
        """
        search = JobDocument.search()

        # Full-text search
        if query:
            q = Q(
                "multi_match",
                query=query,
                fields=[
                    "title^3",          # boost title
                    "description",
                    "employer.username",
                ],
                fuzziness="AUTO",      # fuzzy matching
            )
            search = search.query(q)

        # Filter by job status
        if status:
            search = search.filter("term", status=status)

        # Filter by employer username
        if employer:
            search = search.filter("match", employer__username=employer)

        return search.to_queryset()
