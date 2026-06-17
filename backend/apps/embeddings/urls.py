from django.urls import path

from apps.embeddings import views


urlpatterns = [
    path("similarity/", views.EmbeddingSimilarityView.as_view(), name="embedding-similarity"),
    path("neighbors/", views.EmbeddingNeighborsView.as_view(), name="embedding-neighbors"),
    path("warm/", views.EmbeddingWarmStartView.as_view(), name="embedding-warm"),
    path("status/", views.EmbeddingModelStatusView.as_view(), name="embedding-status"),
]
