from django.core.cache import cache
from uuid import UUID

from django.db.models import Count, Q, QuerySet, Sum

from apps.words.models import Word

WORD_LIST_CACHE_PREFIX = "words:list"
WORD_DETAIL_CACHE_PREFIX = "words:detail"
WORD_LIST_CACHE_REGISTRY = "words:list:registry"
WORD_CACHE_TIMEOUT = 60 * 10


class WordService:
    @staticmethod
    def queryset() -> QuerySet[Word]:
        return Word.objects.select_related("language").all()

    @staticmethod
    def filtered_queryset(params) -> QuerySet[Word]:
        queryset = WordService.queryset()
        language = params.get("language") or params.get("language_code")
        pos = params.get("pos")
        source = params.get("source")

        if language:
            language_filter = Q(language__code__iexact=language)
            try:
                language_filter |= Q(language__id=UUID(str(language)))
            except ValueError:
                pass
            queryset = queryset.filter(language_filter)
        if pos:
            queryset = queryset.filter(pos__iexact=pos)
        if source:
            queryset = queryset.filter(source__iexact=source)
        return queryset

    @staticmethod
    def search(query: str) -> QuerySet[Word]:
        queryset = WordService.queryset()
        if not query:
            return queryset
        return queryset.filter(
            Q(word__icontains=query)
            | Q(lemma__icontains=query)
            | Q(root__icontains=query)
            | Q(ipa__icontains=query)
            | Q(meaning__icontains=query)
            | Q(notes__icontains=query)
            | Q(language__name__icontains=query)
            | Q(language__code__icontains=query)
        )

    @staticmethod
    def create(data: dict) -> Word:
        word = Word.objects.create(**data)
        WordService.clear_cache()
        return word

    @staticmethod
    def update(word: Word, data: dict) -> Word:
        for attr, value in data.items():
            setattr(word, attr, value)
        word.save()
        WordService.clear_cache(word.id)
        return word

    @staticmethod
    def delete(word: Word) -> None:
        word_id = word.id
        word.delete()
        WordService.clear_cache(word_id)

    @staticmethod
    def statistics() -> dict:
        queryset = Word.objects.select_related("language")
        by_language = list(
            queryset.values("language__code", "language__name")
            .annotate(total=Count("id"), total_frequency=Sum("frequency"))
            .order_by("language__name")
        )
        by_pos = list(queryset.values("pos").annotate(total=Count("id")).order_by("pos"))
        return {
            "total_words": queryset.count(),
            "languages": by_language,
            "parts_of_speech": by_pos,
            "sources": list(queryset.order_by("source").values_list("source", flat=True).distinct()),
        }

    @staticmethod
    def list_cache_key(query_params) -> str:
        key = f"{WORD_LIST_CACHE_PREFIX}:{query_params.urlencode()}"
        WordService._remember_list_cache_key(key)
        return key

    @staticmethod
    def detail_cache_key(word_id) -> str:
        return f"{WORD_DETAIL_CACHE_PREFIX}:{word_id}"

    @staticmethod
    def clear_cache(word_id=None) -> None:
        list_keys = cache.get(WORD_LIST_CACHE_REGISTRY, set())
        if list_keys:
            cache.delete_many(list(list_keys))
        cache.delete(WORD_LIST_CACHE_REGISTRY)
        if word_id:
            cache.delete(WordService.detail_cache_key(word_id))

    @staticmethod
    def _remember_list_cache_key(key: str) -> None:
        keys = cache.get(WORD_LIST_CACHE_REGISTRY, set())
        keys.add(key)
        cache.set(WORD_LIST_CACHE_REGISTRY, keys, WORD_CACHE_TIMEOUT)
