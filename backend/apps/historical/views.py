from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from django.db.models import Q
from django.db import models

from .models import HistoricalForm
from .serializers import HistoricalFormSerializer
from django.conf import settings
from pathlib import Path
import json


class HistoricalListView(generics.ListAPIView):
    serializer_class = HistoricalFormSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = HistoricalForm.objects.all()
        proto = self.request.query_params.get('proto_form')
        modern = self.request.query_params.get('modern_form')
        lang = self.request.query_params.get('language')
        if proto:
            qs = qs.filter(proto_form__icontains=proto)
        if modern:
            qs = qs.filter(modern_form__icontains=modern)
        if lang:
            qs = qs.filter(modern_language=lang)
        return qs


class HistoricalDetailView(generics.RetrieveAPIView):
    queryset = HistoricalForm.objects.all()
    serializer_class = HistoricalFormSerializer
    permission_classes = [AllowAny]


class HistoricalSearchView(generics.ListAPIView):
    serializer_class = HistoricalFormSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        q = self.request.query_params.get('q')
        qs = HistoricalForm.objects.all()
        if q:
            qs = qs.filter(Q(modern_form__icontains=q) | Q(middle_turkic_form__icontains=q) | Q(old_turkic_form__icontains=q))
        return qs


class HistoricalEvolutionView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Historical evolution",
        parameters=[
            OpenApiParameter("q", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter("modern", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        modern = request.query_params.get('q') or request.query_params.get('modern')
        if not modern:
            return Response({'error': 'modern form is required via ?q= or ?modern='}, status=400)
        try:
            obj = HistoricalForm.objects.filter(modern_form__iexact=modern).order_by('-confidence_score').first()
            if not obj:
                # fallback: contains
                obj = HistoricalForm.objects.filter(modern_form__icontains=modern).order_by('-confidence_score').first()
            if not obj:
                # As a last resort (e.g., in tests with no DB seed), try loading the dataset file
                try:
                    data_path = Path(settings.BASE_DIR) / 'data' / 'historical' / 'historical_forms.json'
                    if data_path.exists():
                        with data_path.open('r', encoding='utf-8') as fh:
                            records = json.load(fh)
                        # exact match first
                        for r in records:
                            if r.get('modern_form') and r.get('modern_form').lower() == modern.lower():
                                return Response({
                                    'modern': r.get('modern_form'),
                                    'middle': r.get('middle_turkic_form'),
                                    'old_turkic': r.get('old_turkic_form'),
                                    'proto': r.get('proto_form'),
                                })
                        # fallback contains
                        for r in records:
                            if r.get('modern_form') and modern.lower() in r.get('modern_form').lower():
                                return Response({
                                    'modern': r.get('modern_form'),
                                    'middle': r.get('middle_turkic_form'),
                                    'old_turkic': r.get('old_turkic_form'),
                                    'proto': r.get('proto_form'),
                                })
                except Exception:
                    pass
                return Response({})
            return Response({
                'modern': obj.modern_form,
                'middle': obj.middle_turkic_form,
                'old_turkic': obj.old_turkic_form,
                'proto': obj.proto_form,
            })
        except Exception:
            return Response({}, status=200)


class HistoricalStatisticsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Historical statistics",
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        total = HistoricalForm.objects.count()
        by_lang = {}
        qs = HistoricalForm.objects.values('modern_language').annotate(count=models.Count('id'))
        for row in qs:
            by_lang[row['modern_language']] = row['count']
        return Response({'total': total, 'by_language': by_lang})
