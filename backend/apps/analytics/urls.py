from django.urls import path

from apps.analytics import views

urlpatterns = [
    path("feedback/", views.FeedbackCreateView.as_view(), name="feedback-create"),
    path("admin/feedback/", views.AdminFeedbackListView.as_view(), name="admin-feedback"),
    path("admin/qa-errors/", views.AdminQaErrorListView.as_view(), name="admin-qa-errors"),
    path("admin/analytics/events/", views.AnalyticsEventListView.as_view(), name="admin-analytics-events"),
    path("admin/analytics/usage/", views.UsageStatisticsView.as_view(), name="admin-usage-statistics"),
    path("admin/analytics/qa-trends/", views.QaAccuracyTrendsView.as_view(), name="admin-qa-trends"),
    path("admin/analytics/most-requested-words/", views.MostRequestedWordsView.as_view(), name="admin-most-requested-words"),
    path("admin/analytics/most-requested-languages/", views.MostRequestedLanguagesView.as_view(), name="admin-most-requested-languages"),
    path("analytics/health/", views.AnalyticsHealthView.as_view(), name="analytics-health"),
]
