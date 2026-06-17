from django.urls import path

from .views import (
    AdminSeedWordsView,
    AdminWordDetailView,
    AdminWordExportView,
    AdminWordImportBenchmarkView,
    AdminWordListCreateView,
    WordDetailView,
    WordListView,
    WordQualityView,
    WordSearchView,
    WordStatisticsView,
)

urlpatterns = [
    path("words/", WordListView.as_view(), name="word-list"),
    path("words/search/", WordSearchView.as_view(), name="word-search"),
    path("words/statistics/", WordStatisticsView.as_view(), name="word-statistics"),
    path("words/quality/", WordQualityView.as_view(), name="word-quality"),
    path("words/<uuid:id>/", WordDetailView.as_view(), name="word-detail"),
    path("admin/words/", AdminWordListCreateView.as_view(), name="admin-word-list"),
    path("admin/words/export/", AdminWordExportView.as_view(), name="admin-word-export"),
    path("admin/words/benchmark-import/", AdminWordImportBenchmarkView.as_view(), name="admin-word-benchmark-import"),
    path("admin/words/<uuid:id>/", AdminWordDetailView.as_view(), name="admin-word-detail"),
    path("admin/seed/words/", AdminSeedWordsView.as_view(), name="admin-seed-words"),
]
