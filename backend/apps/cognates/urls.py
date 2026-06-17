from django.urls import path
from . import views

app_name = 'cognates'

urlpatterns = [
    path('', views.CognateListView.as_view(), name='list'),
    path('statistics/', views.CognateStatisticsView.as_view(), name='statistics'),
    path('search/', views.CognateSearchView.as_view(), name='search'),
    path('universal-search/', views.UniversalCognateSearchView.as_view(), name='universal-search'),
    path('<uuid:pk>/', views.CognateDetailView.as_view(), name='detail'),
]
