from django.urls import path
from .views import CorpusStatisticsView

app_name = 'corpus'

urlpatterns = [
    path('statistics/', CorpusStatisticsView.as_view(), name='statistics'),
]
