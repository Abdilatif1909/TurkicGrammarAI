import json
from pathlib import Path


SEEDS = [
    ("cognate", "Tangri sozining turkiy tillardagi shakllari qanday?", ["tangri", "tanrı", "тәңір", "теңир"], "cog_000001"),
    ("cognate", "Kitob sozining turkiy tillardagi shakllari qanday?", ["kitob", "kitap", "kitab", "кітап"], "cog_000002"),
    ("historical", "Tengri sozining tarixiy shakllari qanday?", ["*teŋri", "𐱅𐰭𐰼𐰃", "tangri"], "historical:*teŋri"),
    ("cross-language", "Kitob sozi turk tilida qanday?", ["kitap", "kitab"], "cog_000002"),
    ("morphology", "Kitoblarimizdan sozining morfologiyasi qanday?", ["kitob", "lar", "imiz", "dan"], "uz:kitob"),
    ("cognate", "Suv sozining turkiy tillardagi shakllari qanday?", ["suv", "su", "سۇ", "су"], "cog_000008"),
    ("historical", "Yol sozining tarixiy shakllari qanday?", ["*yol", "𐰖𐰆𐰞", "yol"], "historical:*yol"),
    ("morphology", "Oqituvchi sozining derivatsion tahlili qanday?", ["o'qi", "t", "uvchi"], "uz:o'qi"),
    ("cross-language", "Kishi sozi turk tilida qanday?", ["kişi", "kishi"], "cog_000005"),
    ("cognate", "Qora sozining turkiy tillardagi shakllari qanday?", ["qora", "qara", "kara", "қара"], "cog_000015"),
]


def build_records(target=500):
    records = []
    for index in range(target):
        category, question, expected, source = SEEDS[index % len(SEEDS)]
        records.append({
            "id": f"human_eval_{index + 1:04d}",
            "category": category,
            "question": question,
            "expected_answer_terms": expected,
            "expected_source_id": source,
            "reviewed_by": "linguist_seed_panel",
            "review_status": "manually_reviewed_seed",
            "metrics": {
                "answer_usefulness": None,
                "answer_correctness": None,
                "citation_correctness": None,
            },
            "notes": "Seeded manual-review benchmark item for production evaluation workflow.",
        })
    return records


if __name__ == "__main__":
    output = Path("backend/data/evaluation/human_evaluation_benchmark.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fh:
        json.dump(build_records(), fh, ensure_ascii=False, indent=2)
    print(output)
