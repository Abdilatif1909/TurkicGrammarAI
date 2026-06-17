from django.urls import path
from . import views

urlpatterns = [
    path('', views.HistoricalListView.as_view(), name='historical-list'),
    path('search/', views.HistoricalSearchView.as_view(), name='historical-search'),
    path('statistics/', views.HistoricalStatisticsView.as_view(), name='historical-statistics'),
    path('evolution/', views.HistoricalEvolutionView.as_view(), name='historical-evolution'),
    path('<int:pk>/', views.HistoricalDetailView.as_view(), name='historical-detail'),
]
