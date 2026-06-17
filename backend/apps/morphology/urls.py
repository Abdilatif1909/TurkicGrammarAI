from django.urls import path
from apps.morphology import views

urlpatterns = [
    path("analyze/", views.AnalyzeView.as_view(), name="morphology-analyze"),
    path("universal-analyze/", views.UniversalAnalyzeView.as_view(), name="morphology-universal-analyze"),
    path("batch-analyze/", views.BatchAnalyzeView.as_view(), name="morphology-batch-analyze"),
    path("statistics/", views.StatisticsView.as_view(), name="morphology-statistics"),
]
