"""Vector utilities for FastText evaluation."""

from __future__ import annotations

import numpy as np


def normalized_vocab_matrix(kv) -> tuple[list[str], np.ndarray, dict[str, int]]:
    tokens = list(kv.index_to_key)
    matrix = kv.vectors.astype(np.float32, copy=True)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    matrix /= norms
    return tokens, matrix, {token: index for index, token in enumerate(tokens)}


def topn_for_queries(kv, queries: set[str], topn: int = 10) -> dict[str, list[str]]:
    tokens, matrix, token_to_index = normalized_vocab_matrix(kv)
    results: dict[str, list[str]] = {}
    for query in sorted(queries):
        if query not in token_to_index:
            continue
        query_vector = matrix[token_to_index[query]]
        scores = matrix @ query_vector
        scores[token_to_index[query]] = -np.inf
        candidate_count = min(topn, len(tokens) - 1)
        top_indexes = np.argpartition(-scores, candidate_count)[:candidate_count]
        top_indexes = top_indexes[np.argsort(-scores[top_indexes])]
        results[query] = [tokens[index] for index in top_indexes[:topn]]
    return results


def has_relevant(neighbors: list[str], relevant_forms: set[str], k: int) -> bool:
    return bool(set(neighbors[:k]) & relevant_forms)
