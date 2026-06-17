from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.embeddings.views import SemanticSearchView, TurkicQaAskView, TurkicRagRetrieveView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.languages.urls")),
    path("api/corpus/", include("apps.corpus.urls")),
    path("api/cognates/", include("apps.cognates.urls")),
    path("api/historical/", include("apps.historical.urls")),
    path("api/morphology/", include("apps.morphology.urls")),
    path("api/embeddings/", include("apps.embeddings.urls")),
    path("api/search/semantic/", SemanticSearchView.as_view(), name="semantic-search"),
    path("api/rag/retrieve/", TurkicRagRetrieveView.as_view(), name="rag-retrieve"),
    path("api/qa/ask/", TurkicQaAskView.as_view(), name="qa-ask"),
    path("api/", include("apps.analytics.urls")),
    path("api/", include("apps.words.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
