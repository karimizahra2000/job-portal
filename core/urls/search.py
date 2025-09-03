# core/urls.py
from django.urls import path
from core.views.search import JobSearchView

urlpatterns = [
    path("jobs/", JobSearchView.as_view(), name="job-search"),
]
