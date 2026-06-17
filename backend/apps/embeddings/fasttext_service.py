import os
import threading
import time
from functools import lru_cache
from pathlib import Path
from typing import Dict

from gensim.models import FastText


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL = PROJECT_ROOT / "backend/models/turkic_fasttext.model"
_LOAD_LOCK = threading.Lock()
_MODEL_STATUS = {
    "loaded": False,
    "model_path": str(DEFAULT_MODEL),
    "load_time_ms": None,
    "vocabulary_size": None,
}


@lru_cache(maxsize=1)
def load_fasttext_model(model_path: str = str(DEFAULT_MODEL)) -> FastText:
    with _LOAD_LOCK:
        start = time.perf_counter()
        mmap_mode = os.getenv("FASTTEXT_MMAP_MODE") or None
        model = FastText.load(model_path, mmap=mmap_mode)
        model.wv.fill_norms(force=True)
        _MODEL_STATUS.update(
            {
                "loaded": True,
                "model_path": model_path,
                "load_time_ms": round((time.perf_counter() - start) * 1000, 3),
                "vocabulary_size": len(model.wv.index_to_key),
            }
        )
        return model


def warm_fasttext_model(model_path: str = str(DEFAULT_MODEL)) -> Dict:
    load_fasttext_model(model_path)
    return model_status()


def model_status() -> Dict:
    return dict(_MODEL_STATUS)


def similarity(word_a: str, word_b: str, model_path: str = str(DEFAULT_MODEL)) -> Dict:
    model = load_fasttext_model(model_path)
    score = float(model.wv.similarity(word_a, word_b))
    return {
        "word_a": word_a,
        "word_b": word_b,
        "similarity": round(score, 6),
        "model": model_path,
    }


def nearest_neighbors(word: str, topn: int = 10, model_path: str = str(DEFAULT_MODEL)) -> Dict:
    model = load_fasttext_model(model_path)
    neighbors = [
        {"word": token, "score": round(float(score), 6)}
        for token, score in model.wv.most_similar(word, topn=topn)
    ]
    return {"word": word, "neighbors": neighbors}
