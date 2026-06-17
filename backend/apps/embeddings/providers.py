from abc import ABC, abstractmethod
from typing import Dict, Iterable, List, Sequence


class EmbeddingProvider(ABC):
    name = "base"

    def __init__(self, vector_size: int = 300, **options):
        self.vector_size = vector_size
        self.options = options
        self.is_trained = False

    @abstractmethod
    def fit(self, records: Iterable[Dict]):
        raise NotImplementedError

    @abstractmethod
    def encode(self, tokens: Sequence[str]) -> List[List[float]]:
        raise NotImplementedError

    def save(self, path: str) -> None:
        raise NotImplementedError(f"{self.name} persistence is not implemented until the training phase")

    def load(self, path: str):
        raise NotImplementedError(f"{self.name} loading is not implemented until the training phase")


class FastTextProvider(EmbeddingProvider):
    name = "fasttext"

    def fit(self, records: Iterable[Dict]):
        self.is_trained = False
        return {
            "provider": self.name,
            "status": "not_trained",
            "reason": "Phase 19 defines the provider contract only; training is deferred.",
        }

    def encode(self, tokens: Sequence[str]) -> List[List[float]]:
        if not self.is_trained:
            raise RuntimeError("FastTextProvider is not trained yet")
        return []


class Word2VecProvider(EmbeddingProvider):
    name = "word2vec"

    def fit(self, records: Iterable[Dict]):
        self.is_trained = False
        return {
            "provider": self.name,
            "status": "not_trained",
            "reason": "Phase 19 defines the provider contract only; training is deferred.",
        }

    def encode(self, tokens: Sequence[str]) -> List[List[float]]:
        if not self.is_trained:
            raise RuntimeError("Word2VecProvider is not trained yet")
        return []


class TransformerProvider(EmbeddingProvider):
    name = "transformer"

    def fit(self, records: Iterable[Dict]):
        self.is_trained = False
        return {
            "provider": self.name,
            "status": "not_trained",
            "reason": "Phase 19 defines the provider contract only; fine-tuning is deferred.",
        }

    def encode(self, tokens: Sequence[str]) -> List[List[float]]:
        if not self.is_trained:
            raise RuntimeError("TransformerProvider is not initialized with a model yet")
        return []


PROVIDERS = {
    FastTextProvider.name: FastTextProvider,
    Word2VecProvider.name: Word2VecProvider,
    TransformerProvider.name: TransformerProvider,
}
