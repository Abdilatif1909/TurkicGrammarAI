from django.urls import path

from .views import (
    AdminLanguageDetailView,
    AdminLanguageExportView,
    AdminLanguageListCreateView,
    AdminSeedLanguagesView,
    LanguageDetailView,
    LanguageListView,
    LanguageSearchView,
    LanguageStatisticsView,
)

urlpatterns = [
    path("languages/", LanguageListView.as_view(), name="language-list"),
    path("languages/search/", LanguageSearchView.as_view(), name="language-search"),
    path("languages/statistics/", LanguageStatisticsView.as_view(), name="language-statistics"),
    path("languages/<uuid:id>/", LanguageDetailView.as_view(), name="language-detail"),
    path("admin/languages/", AdminLanguageListCreateView.as_view(), name="admin-language-list"),
    path("admin/languages/export/", AdminLanguageExportView.as_view(), name="admin-language-export"),
    path("admin/languages/<uuid:id>/", AdminLanguageDetailView.as_view(), name="admin-language-detail"),
    path("admin/seed/languages/", AdminSeedLanguagesView.as_view(), name="admin-seed-languages"),
]
