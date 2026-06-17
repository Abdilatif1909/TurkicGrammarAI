import json
import re
import sys
from pathlib import Path
from typing import Dict, List

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from apps.embeddings.turkic_retriever import retrieve


STOPWORDS = {
    "qanday", "qanaqa", "nima", "nima?", "so'z", "soz", "sozi", "so'zining",
    "shakli", "shakllari", "tarixiy", "tarixi", "tillardagi", "turkiy",
    "tillar", "tillarda", "tilida", "turk", "boshqa", "ning", "dagi", "lar",
    "qa", "mi", "bor", "qaysi", "ko'rsat", "korsat", "haqida",
}

LANGUAGE_NAMES = {
    "uz": "Uzbek",
    "tr": "Turkish",
    "az": "Azerbaijani",
    "kk": "Kazakh",
    "ky": "Kyrgyz",
    "tk": "Turkmen",
    "ug": "Uyghur",
    "otk": "Old Turkic",
}


def _tokens(question: str) -> List[str]:
    return [
        token.strip("'\"`.,?!:;()[]{}").lower()
        for token in re.split(r"\s+", question or "")
        if token.strip("'\"`.,?!:;()[]{}")
    ]


def infer_question_type(question: str) -> str:
    lowered = (question or "").lower()
    if any(term in lowered for term in ("tarix", "histor", "proto", "old turkic", "qadimgi")):
        return "historical"
    if any(term in lowered for term in ("turk til", "turkish", "boshqa til", "cross")):
        return "cross-language"
    if any(term in lowered for term in ("qo'shimcha", "qoshimcha", "morfolog", "suffix", "root", "ildiz")):
        return "morphology"
    return "cognate"


def extract_query_term(question: str, topn: int = 8) -> Dict:
    candidates = []
    for token in _tokens(question):
        if len(token) < 2 or token in STOPWORDS:
            continue
        candidates.append(token)
    if not candidates:
        candidates = _tokens(question)[:4] or [question]

    best = None
    for token in dict.fromkeys(candidates):
        payload = retrieve(token, topn=topn)
        docs = payload.get("retrieved_documents", [])
        if not docs:
            continue
        score = docs[0].get("final_relevance_score", docs[0].get("score", 0))
        if best is None or score > best["score"]:
            best = {"term": token, "score": score, "payload": payload}

    if best:
        return best
    payload = retrieve(question, topn=topn)
    return {"term": question, "score": 0, "payload": payload}


def _citation(document: Dict) -> Dict:
    return {
        "source_type": document.get("source_type", "semantic"),
        "source_id": document.get("source_id", ""),
        "confidence": document.get("confidence", 0),
    }


def _answer_item(document: Dict) -> Dict:
    return {
        "lemma": document.get("lemma", ""),
        "word": document.get("word", ""),
        "root": document.get("root", ""),
        "language": document.get("language", ""),
        "language_name": LANGUAGE_NAMES.get(document.get("language", ""), document.get("language", "")),
        "cognate_group": document.get("cognate_group", ""),
        "historical_lineage": document.get("historical_lineage", []),
        "similarity": document.get("similarity", 0),
        "final_relevance_score": document.get("final_relevance_score", document.get("score", 0)),
        "source_type": document.get("source_type", "semantic"),
        "source_id": document.get("source_id", ""),
        "confidence": document.get("confidence", 0),
        "source_trace": document.get("source_trace", []),
    }


def build_answer(question: str, retrieval_payload: Dict, question_type: str) -> Dict:
    documents = retrieval_payload.get("retrieved_documents", [])
    answer_items = [_answer_item(document) for document in documents[:10]]
    citations = [_citation(document) for document in documents[:10]]
    top = answer_items[0] if answer_items else {}

    if not answer_items:
        answer_text = "No reliable Turkic linguistic evidence was found for this question."
    elif question_type == "historical":
        lineage = top.get("historical_lineage", [])
        forms = [item.get("form") for item in lineage if item.get("form")]
        answer_text = f"{top.get('lemma', '')} historical lineage: " + ", ".join(forms[:8])
    elif question_type == "cross-language":
        forms = [f"{item['language_name']}: {item['word']}" for item in answer_items[:8]]
        answer_text = "Cross-language forms: " + "; ".join(forms)
    elif question_type == "morphology":
        forms = [f"{item['word']} (root={item.get('root', '')}, {item['language_name']})" for item in answer_items[:8]]
        answer_text = "Morphological evidence: " + "; ".join(forms)
    else:
        forms = [f"{item['language_name']}: {item['word']}" for item in answer_items[:8]]
        answer_text = f"Cognate group {top.get('cognate_group', '')}: " + "; ".join(forms)

    return {
        "answer": answer_text,
        "answer_type": question_type,
        "items": answer_items,
        "citations": citations,
    }


def ask(question: str, topk: int = 10) -> Dict:
    question = (question or "").strip()
    if not question:
        return {"question": question, "answer": "", "items": [], "citations": []}
    question_type = infer_question_type(question)
    selected = extract_query_term(question, topn=max(topk, 10))
    answer = build_answer(question, selected["payload"], question_type)
    return {
        "question": question,
        "query_term": selected["term"],
        "question_type": question_type,
        "answer": answer["answer"],
        "items": answer["items"][:topk],
        "citations": answer["citations"][:topk],
        "support_documents": selected["payload"].get("retrieved_documents", [])[:topk],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ask retrieval-based Turkic QA")
    parser.add_argument("question")
    parser.add_argument("--topk", type=int, default=10)
    args = parser.parse_args()
    print(json.dumps(ask(args.question, args.topk), ensure_ascii=False, indent=2))
