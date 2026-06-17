from django.core.cache import cache
from django.db.models import Q, QuerySet

from apps.languages.models import Language

LANGUAGE_LIST_CACHE_PREFIX = "languages:list"
LANGUAGE_DETAIL_CACHE_PREFIX = "languages:detail"
LANGUAGE_LIST_CACHE_REGISTRY = "languages:list:registry"
LANGUAGE_CACHE_TIMEOUT = 60 * 15


class LanguageService:
    @staticmethod
    def active_queryset() -> QuerySet[Language]:
        return Language.objects.filter(is_active=True)

    @staticmethod
    def filtered_queryset(params) -> QuerySet[Language]:
        queryset = LanguageService.active_queryset()
        for field in ("code", "family", "branch", "country"):
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__iexact": value})
        return queryset

    @staticmethod
    def search(query: str) -> QuerySet[Language]:
        queryset = LanguageService.active_queryset()
        if not query:
            return queryset
        return queryset.filter(
            Q(name__icontains=query)
            | Q(native_name__icontains=query)
            | Q(code__icontains=query)
            | Q(iso639_3__icontains=query)
            | Q(family__icontains=query)
            | Q(branch__icontains=query)
            | Q(country__icontains=query)
        )

    @staticmethod
    def create(data: dict) -> Language:
        language = Language.objects.create(**data)
        LanguageService.clear_cache()
        return language

    @staticmethod
    def update(language: Language, data: dict) -> Language:
        for attr, value in data.items():
            setattr(language, attr, value)
        language.save()
        LanguageService.clear_cache(language.id)
        return language

    @staticmethod
    def deactivate(language: Language) -> Language:
        language.is_active = False
        language.save(update_fields=["is_active", "updated_at"])
        LanguageService.clear_cache(language.id)
        return language

    @staticmethod
    def statistics() -> dict:
        queryset = LanguageService.active_queryset()
        return {
            "total_languages": queryset.count(),
            "families": list(queryset.order_by("family").values_list("family", flat=True).distinct()),
            "countries": list(queryset.order_by("country").values_list("country", flat=True).distinct()),
        }

    @staticmethod
    @staticmethod
    def list_cache_key(query_params) -> str:
        encoded = query_params.urlencode()
        key = f"{LANGUAGE_LIST_CACHE_PREFIX}:{encoded}"
        LanguageService._remember_list_cache_key(key)
        return key

    @staticmethod
    def detail_cache_key(language_id) -> str:
        return f"{LANGUAGE_DETAIL_CACHE_PREFIX}:{language_id}"

    @staticmethod
    def clear_cache(language_id=None) -> None:
        list_keys = cache.get(LANGUAGE_LIST_CACHE_REGISTRY, set())
        if list_keys:
            cache.delete_many(list(list_keys))
        cache.delete(LANGUAGE_LIST_CACHE_REGISTRY)
        if language_id:
            cache.delete(LanguageService.detail_cache_key(language_id))

    @staticmethod
    def _remember_list_cache_key(key: str) -> None:
        keys = cache.get(LANGUAGE_LIST_CACHE_REGISTRY, set())
        keys.add(key)
        cache.set(LANGUAGE_LIST_CACHE_REGISTRY, keys, LANGUAGE_CACHE_TIMEOUT)
