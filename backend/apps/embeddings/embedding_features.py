from dataclasses import dataclass, field
from typing import Dict, Iterable, List


LANGUAGES = ["uz", "tr", "az", "kk", "ky", "tk", "ug", "otk"]
MORPHOLOGY_FEATURES = [
    "NOUN",
    "VERB",
    "ADJECTIVE",
    "PLURAL",
    "POSS_1SG",
    "POSS_2SG",
    "POSS_3SG",
    "POSS_1PL",
    "POSS_2PL",
    "POSS_3PL",
    "DATIVE",
    "ACCUSATIVE",
    "LOCATIVE",
    "ABLATIVE",
    "GENITIVE",
    "PAST",
    "PRESENT",
    "FUTURE",
    "CONVERB",
    "CONDITIONAL",
    "NEGATIVE",
    "DERIVATIONAL",
]


@dataclass
class EmbeddingFeatureEncoder:
    language_ids: Dict[str, int] = field(default_factory=lambda: {lang: i for i, lang in enumerate(LANGUAGES)})
    morphology_feature_ids: Dict[str, int] = field(default_factory=lambda: {feature: i for i, feature in enumerate(MORPHOLOGY_FEATURES)})
    lemma_ids: Dict[str, int] = field(default_factory=dict)
    root_ids: Dict[str, int] = field(default_factory=dict)
    cognate_ids: Dict[str, int] = field(default_factory=dict)

    def fit(self, records: Iterable[Dict]) -> "EmbeddingFeatureEncoder":
        for record in records:
            self._id_for(self.lemma_ids, record.get("lemma") or "")
            self._id_for(self.root_ids, record.get("root") or "")
            self._id_for(self.cognate_ids, record.get("cognate_group") or "")
        return self

    def encode(self, record: Dict) -> Dict:
        features = record.get("features") or []
        return {
            "language_id": self.language_ids.get(record.get("language"), -1),
            "lemma_id": self._id_for(self.lemma_ids, record.get("lemma") or ""),
            "root_id": self._id_for(self.root_ids, record.get("root") or ""),
            "cognate_id": self._id_for(self.cognate_ids, record.get("cognate_group") or ""),
            "morphology_feature_ids": [
                self.morphology_feature_ids[feature]
                for feature in features
                if feature in self.morphology_feature_ids
            ],
            "morphology_feature_vector": self.multi_hot(features),
        }

    def multi_hot(self, features: List[str]) -> List[int]:
        vector = [0] * len(self.morphology_feature_ids)
        for feature in features:
            idx = self.morphology_feature_ids.get(feature)
            if idx is not None:
                vector[idx] = 1
        return vector

    @staticmethod
    def _id_for(mapping: Dict[str, int], value: str) -> int:
        if value not in mapping:
            mapping[value] = len(mapping)
        return mapping[value]

    def schema(self) -> Dict:
        return {
            "language_ids": self.language_ids,
            "morphology_feature_ids": self.morphology_feature_ids,
            "lemma_count": len(self.lemma_ids),
            "root_count": len(self.root_ids),
            "cognate_count": len(self.cognate_ids),
        }
