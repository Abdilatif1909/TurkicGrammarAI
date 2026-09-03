"""Template-based QA engine for generated benchmarks."""

from __future__ import annotations

from pathlib import Path
import re
import sys


if str(Path(__file__).resolve().parents[1] / "evaluation") not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parents[1] / "evaluation"))

from common import compact_entry, load_jsonl  # noqa: E402
from vector_utils import topn_for_queries  # noqa: E402


COGNATE_RE = re.compile(
    r"^Which language\(s\) share a cognate with '(.+)' \((.+)\)\?$"
)
LEMMA_RE = re.compile(r"^What is the lemma of '(.+)' in (.+)\?$")
LINEAGE_RE = re.compile(
    r"^Which modern language\(s\) have descendants linked to Old Turkic '(.+)'\?$"
)


class SimpleQAEngine:
    def __init__(self, project_root: Path) -> None:
        self.entries = load_jsonl(
            project_root / "data" / "processed" / "lexicon_master_full.jsonl"
        )
        self.groups = load_jsonl(
            project_root / "data" / "processed" / "cognate_groups.jsonl"
        )
        self.lineage_links = load_jsonl(
            project_root / "data" / "processed" / "lineage_links.jsonl"
        )
        self.entry_index = {
            (entry["surface_form"], entry["language"]): entry
            for entry in self.entries
        }
        self.groups_by_id = {group["cognate_id"]: group for group in self.groups}
        self.lineage_by_id = {
            link["lineage_id"]: link for link in self.lineage_links
        }
        self.lineage_by_old_form = {
            link["old_turkic_form"]: link for link in self.lineage_links
        }

    def answer(self, question: str) -> dict:
        if match := COGNATE_RE.match(question):
            return self._answer_cognate_languages(match.group(1), match.group(2))
        if match := LEMMA_RE.match(question):
            return self._answer_lemma(match.group(1), match.group(2))
        if match := LINEAGE_RE.match(question):
            return self._answer_lineage_languages(match.group(1))
        return {
            "generated_answer": "",
            "supporting_entries": [],
            "source_ids": [],
        }

    def _answer_cognate_languages(self, form: str, language: str) -> dict:
        entry = self.entry_index.get((form, language))
        if not entry or not entry.get("cognate_ids"):
            return {"generated_answer": "", "supporting_entries": [], "source_ids": []}
        group_id = entry["cognate_ids"][0]
        group = self.groups_by_id[group_id]
        languages = sorted(
            {
                member["language"]
                for member in group["member_entries"]
                if member["language"] != language
            }
        )
        return {
            "generated_answer": ", ".join(languages),
            "supporting_entries": [
                {"form": item["surface_form"], "lang": item["language"], "lemma": item["lemma"]}
                for item in group["member_entries"]
            ],
            "source_ids": [group_id],
        }

    def _answer_lemma(self, form: str, language: str) -> dict:
        entry = self.entry_index.get((form, language))
        if not entry:
            return {"generated_answer": "", "supporting_entries": [], "source_ids": []}
        return {
            "generated_answer": entry.get("lemma") or "",
            "supporting_entries": [compact_entry(entry)],
            "source_ids": entry.get("cognate_ids", []),
        }

    def _answer_lineage_languages(self, old_turkic_form: str) -> dict:
        link = self.lineage_by_old_form.get(old_turkic_form)
        if not link:
            return {"generated_answer": "", "supporting_entries": [], "source_ids": []}
        languages = sorted(
            {member["language"] for member in link["descendant_entries"]}
        )
        return {
            "generated_answer": ", ".join(languages),
            "supporting_entries": [
                {"form": item["surface_form"], "lang": item["language"], "lemma": item["lemma"]}
                for item in link["old_turkic_entries"] + link["descendant_entries"]
            ],
            "source_ids": [link["lineage_id"], link["source_cognate_id"]],
        }


class EmbeddingQAEngine(SimpleQAEngine):
    """Answer supported QA templates through nearest-neighbor retrieval only."""

    def __init__(self, project_root: Path, keyed_vectors, topn: int = 10) -> None:
        super().__init__(project_root)
        self.keyed_vectors = keyed_vectors
        self.topn = topn
        self.entries_by_form: dict[str, list[dict]] = {}
        for entry in self.entries:
            self.entries_by_form.setdefault(entry["surface_form"], []).append(entry)

    def answer(self, question: str) -> dict:
        if match := COGNATE_RE.match(question):
            return self._answer_cognate_languages_embedding(match.group(1), match.group(2))
        if LEMMA_RE.match(question):
            return {
                "generated_answer": "",
                "supporting_entries": [],
                "source_ids": [],
                "skipped": True,
                "skip_reason": "lemma_lookup_requires_direct_database_lookup",
            }
        if match := LINEAGE_RE.match(question):
            return self._answer_lineage_languages_embedding(match.group(1))
        return {
            "generated_answer": "",
            "supporting_entries": [],
            "source_ids": [],
        }

    def _neighbors(self, form: str) -> list[str]:
        return topn_for_queries(self.keyed_vectors, {form}, topn=self.topn).get(form, [])

    def _entries_from_neighbor_forms(self, forms: list[str]) -> list[dict]:
        rows = []
        seen = set()
        for form in forms:
            for entry in self.entries_by_form.get(form, []):
                key = (entry["language"], entry["surface_form"])
                if key in seen:
                    continue
                seen.add(key)
                rows.append(entry)
        return rows

    def _answer_cognate_languages_embedding(self, form: str, language: str) -> dict:
        neighbor_entries = self._entries_from_neighbor_forms(self._neighbors(form))
        languages = sorted(
            {
                entry["language"]
                for entry in neighbor_entries
                if entry["language"] != language
            }
        )
        source_ids = sorted(
            {
                cognate_id
                for entry in neighbor_entries
                for cognate_id in entry.get("cognate_ids", [])
            }
        )
        return {
            "generated_answer": ", ".join(languages),
            "supporting_entries": [compact_entry(entry) for entry in neighbor_entries],
            "source_ids": source_ids,
        }

    def _answer_lineage_languages_embedding(self, old_turkic_form: str) -> dict:
        neighbor_entries = self._entries_from_neighbor_forms(self._neighbors(old_turkic_form))
        languages = sorted(
            {
                entry["language"]
                for entry in neighbor_entries
                if entry["language"] != "old_turkic"
            }
        )
        source_ids = sorted(
            {
                source_id
                for entry in neighbor_entries
                for source_id in entry.get("cognate_ids", []) + entry.get("lineage_ids", [])
            }
        )
        return {
            "generated_answer": ", ".join(languages),
            "supporting_entries": [compact_entry(entry) for entry in neighbor_entries],
            "source_ids": source_ids,
        }
