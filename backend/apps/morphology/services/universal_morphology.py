from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

from apps.morphology.services.morphology_service import analyze
from apps.morphology.services.lemma_dictionary import LemmaDictionary


SUPPORTED_LANGUAGES = ["uz", "tr", "az", "kk", "ky", "tk", "ug", "otk"]


@dataclass
class UniversalMorphologicalAnalysis:
    language: str
    surface_form: str
    lemma: str
    root: str
    features: List[str]
    confidence: float

    def to_dict(self) -> Dict:
        return asdict(self)


FEATURE_INVENTORY = {
    "pos": ["NOUN", "VERB", "ADJECTIVE"],
    "nominal": [
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
    ],
    "verbal": ["PAST", "PRESENT", "FUTURE", "CONVERB", "CONDITIONAL", "NEGATIVE"],
    "derivational": ["DERIVATIONAL"],
}


COMMON_SUFFIX_FEATURES = {
    # Oghuz/Karluk Latin
    "lar": "PLURAL",
    "ler": "PLURAL",
    "im": "POSS_1SG",
    "ım": "POSS_1SG",
    "ym": "POSS_1SG",
    "um": "POSS_1SG",
    "üm": "POSS_1SG",
    "in": "POSS_2SG",
    "ın": "POSS_2SG",
    "iň": "POSS_2SG",
    "yň": "POSS_2SG",
    "un": "POSS_2SG",
    "ün": "POSS_2SG",
    "i": "POSS_3SG",
    "ı": "POSS_3SG",
    "y": "POSS_3SG",
    "si": "POSS_3SG",
    "sı": "POSS_3SG",
    "sy": "POSS_3SG",
    "imiz": "POSS_1PL",
    "ımız": "POSS_1PL",
    "ymyz": "POSS_1PL",
    "ümüz": "POSS_1PL",
    "umuz": "POSS_1PL",
    "iňiz": "POSS_2PL",
    "yňyz": "POSS_2PL",
    "iniz": "POSS_2PL",
    "ınız": "POSS_2PL",
    "a": "DATIVE",
    "e": "DATIVE",
    "ga": "DATIVE",
    "ge": "DATIVE",
    "qa": "DATIVE",
    "ke": "DATIVE",
    "ni": "ACCUSATIVE",
    "ny": "ACCUSATIVE",
    "ı": "ACCUSATIVE",
    "i": "ACCUSATIVE",
    "da": "LOCATIVE",
    "de": "LOCATIVE",
    "ta": "LOCATIVE",
    "te": "LOCATIVE",
    "dan": "ABLATIVE",
    "den": "ABLATIVE",
    "tan": "ABLATIVE",
    "ten": "ABLATIVE",
    "ning": "GENITIVE",
    "nyň": "GENITIVE",
    "niň": "GENITIVE",
    "di": "PAST",
    "dı": "PAST",
    "dy": "PAST",
    "ti": "PAST",
    "tı": "PAST",
    "ty": "PAST",
    "ma": "NEGATIVE",
    "me": "NEGATIVE",
    "maz": "NEGATIVE",
    "mez": "NEGATIVE",
    "jak": "FUTURE",
    "jek": "FUTURE",
    "ar": "PRESENT",
    "er": "PRESENT",
    "yp": "CONVERB",
    "ip": "CONVERB",
    "sa": "CONDITIONAL",
    "se": "CONDITIONAL",
    "chi": "DERIVATIONAL",
    "çı": "DERIVATIONAL",
    "çi": "DERIVATIONAL",
    "çy": "DERIVATIONAL",
    "lik": "DERIVATIONAL",
    "lık": "DERIVATIONAL",
    "lyk": "DERIVATIONAL",
    "li": "DERIVATIONAL",
    "siz": "DERIVATIONAL",
    "syz": "DERIVATIONAL",
    "dash": "DERIVATIONAL",
    "daş": "DERIVATIONAL",
}


CYRILLIC_SUFFIX_FEATURES = {
    "лар": "PLURAL",
    "лер": "PLURAL",
    "дар": "PLURAL",
    "дер": "PLURAL",
    "тар": "PLURAL",
    "тер": "PLURAL",
    "лор": "PLURAL",
    "лөр": "PLURAL",
    "ым": "POSS_1SG",
    "ім": "POSS_1SG",
    "ум": "POSS_1SG",
    "үм": "POSS_1SG",
    "ың": "POSS_2SG",
    "ің": "POSS_2SG",
    "уң": "POSS_2SG",
    "үң": "POSS_2SG",
    "ы": "POSS_3SG",
    "і": "POSS_3SG",
    "у": "POSS_3SG",
    "ү": "POSS_3SG",
    "ымыз": "POSS_1PL",
    "іміз": "POSS_1PL",
    "ыбыз": "POSS_1PL",
    "ибиз": "POSS_1PL",
    "убуз": "POSS_1PL",
    "үбүз": "POSS_1PL",
    "ға": "DATIVE",
    "ге": "DATIVE",
    "қа": "DATIVE",
    "ке": "DATIVE",
    "га": "DATIVE",
    "ны": "ACCUSATIVE",
    "ні": "ACCUSATIVE",
    "ды": "ACCUSATIVE",
    "ді": "ACCUSATIVE",
    "ты": "ACCUSATIVE",
    "ті": "ACCUSATIVE",
    "да": "LOCATIVE",
    "де": "LOCATIVE",
    "та": "LOCATIVE",
    "те": "LOCATIVE",
    "дан": "ABLATIVE",
    "ден": "ABLATIVE",
    "тан": "ABLATIVE",
    "тен": "ABLATIVE",
    "нан": "ABLATIVE",
    "нен": "ABLATIVE",
    "дың": "GENITIVE",
    "дің": "GENITIVE",
    "тың": "GENITIVE",
    "тің": "GENITIVE",
    "нын": "GENITIVE",
    "нин": "GENITIVE",
    "ды": "PAST",
    "ді": "PAST",
    "ты": "PAST",
    "ті": "PAST",
    "ма": "NEGATIVE",
    "ме": "NEGATIVE",
    "ба": "NEGATIVE",
    "бе": "NEGATIVE",
    "па": "NEGATIVE",
    "пе": "NEGATIVE",
    "шы": "DERIVATIONAL",
    "ші": "DERIVATIONAL",
    "чы": "DERIVATIONAL",
    "чи": "DERIVATIONAL",
    "лық": "DERIVATIONAL",
    "лік": "DERIVATIONAL",
    "лык": "DERIVATIONAL",
    "лик": "DERIVATIONAL",
    "сыз": "DERIVATIONAL",
    "сіз": "DERIVATIONAL",
    "даш": "DERIVATIONAL",
    "дош": "DERIVATIONAL",
}


ARABIC_SUFFIX_FEATURES = {
    "لار": "PLURAL",
    "لەر": "PLURAL",
    "ىم": "POSS_1SG",
    "ىڭ": "POSS_2SG",
    "ى": "POSS_3SG",
    "ىمىز": "POSS_1PL",
    "ىڭىز": "POSS_2PL",
    "نى": "ACCUSATIVE",
    "غا": "DATIVE",
    "گە": "DATIVE",
    "دا": "LOCATIVE",
    "دە": "LOCATIVE",
    "دىن": "ABLATIVE",
    "دىن": "ABLATIVE",
    "دى": "PAST",
    "غان": "PAST",
    "ما": "NEGATIVE",
    "مە": "NEGATIVE",
    "چى": "DERIVATIONAL",
    "چىلىق": "DERIVATIONAL",
    "لىق": "DERIVATIONAL",
    "لىك": "DERIVATIONAL",
    "سىز": "DERIVATIONAL",
    "داش": "DERIVATIONAL",
}


RUNIFORM_SUFFIX_FEATURES = {
    "\U00010c20\U00010c00\U00010c3c": "PLURAL",
    "\U00010c20\U00010c03\U00010c3c": "PLURAL",
    "\U00010c03\U00010c22": "POSS_1SG",
    "\U00010c03\U00010c22\U00010c03\U00010c1e": "POSS_1PL",
    "\U00010c23": "ACCUSATIVE",
    "\U00010c34\U00010c00": "DATIVE",
    "\U00010c1a\U00010c03": "DATIVE",
    "\U00010c30\U00010c00": "LOCATIVE",
    "\U00010c30\U00010c03": "LOCATIVE",
    "\U00010c30\U00010c03\U00010c23": "ABLATIVE",
    "\U00010c45\U00010c03\U00010c23": "ABLATIVE",
    "\U00010c30\U00010c03": "PAST",
    "\U00010c22\U00010c00": "NEGATIVE",
    "\U00010c22\U00010c03": "NEGATIVE",
    "\U00010c41\U00010c03": "DERIVATIONAL",
    "\U00010c20\U00010c03\U00010c36": "DERIVATIONAL",
}


FEATURE_MAP = {}
FEATURE_MAP.update(COMMON_SUFFIX_FEATURES)
FEATURE_MAP.update(CYRILLIC_SUFFIX_FEATURES)
FEATURE_MAP.update(ARABIC_SUFFIX_FEATURES)
FEATURE_MAP.update(RUNIFORM_SUFFIX_FEATURES)
FEATURE_MAP.update({
    "ты": "PAST",
    "ті": "PAST",
    "ды": "PAST",
    "ді": "PAST",
    "ти": "PAST",
    "ди": "PAST",
    "ны": "ACCUSATIVE",
    "ні": "ACCUSATIVE",
    "ни": "ACCUSATIVE",
    "тү": "ACCUSATIVE",
    "ту": "ACCUSATIVE",
})


def suffix_chain(analysis: Dict) -> List[str]:
    chain = []
    for item in analysis.get("suffixes", []) or []:
        if isinstance(item, dict):
            chain.append(item.get("suffix"))
        else:
            chain.append(item)
    return [s for s in chain if s]


def _lemma_category(root: str, language: Optional[str]) -> Optional[str]:
    if not root or not language:
        return None
    meta = LemmaDictionary.get_meta(root, language=language)
    category = meta.get("category") if meta else None
    return category.lower() if isinstance(category, str) else category


def normalize_features(analysis: Dict, language: Optional[str] = None) -> List[str]:
    features = []
    chain = suffix_chain(analysis)
    category = _lemma_category(analysis.get("root") or "", language)
    for suffix in chain:
        feature = FEATURE_MAP.get(suffix)
        if language in {"kk", "ky"} and suffix in {"ты", "ті", "ды", "ді", "ти", "ди"}:
            if category == "noun":
                feature = "ACCUSATIVE"
        if feature and feature not in features:
            features.append(feature)
    if (analysis.get("type") == "derivational" or analysis.get("derivation_type")) and not features:
        features.append("DERIVATIONAL")
    runic_di = "\U00010c30\U00010c03"
    runic_n = "\U00010c23"
    if runic_di in chain and runic_n in chain and "PAST" in features and "ACCUSATIVE" in features:
        features = [feature for feature in features if feature not in {"PAST", "ACCUSATIVE"}]
        if "ABLATIVE" not in features:
            features.append("ABLATIVE")
    return features


def universal_analyze(surface: str, language: str, max_results: int = 10) -> UniversalMorphologicalAnalysis:
    analyses = analyze(surface, language, max_results=max_results)
    if analyses:
        def analysis_key(item: Dict):
            features = normalize_features(item, language)
            root = item.get("root") or ""
            score = float(item.get("confidence", item.get("score", 0.0)) or 0.0)
            return (
                1 if features else 0,
                1 if len(root) >= 3 else 0,
                len(features),
                score,
                len(suffix_chain(item)),
                1 if LemmaDictionary.is_lemma(root, language=language) else 0,
                min(len(root), 4),
            )

        top = max(
            analyses,
            key=analysis_key,
        )
    else:
        top = {"root": surface, "lemma": surface, "score": 0.0}
    return UniversalMorphologicalAnalysis(
        language=language,
        surface_form=surface,
        lemma=top.get("lemma") or top.get("root") or surface,
        root=top.get("root") or surface,
        features=normalize_features(top, language),
        confidence=round(float(top.get("confidence", top.get("score", 0.0)) or 0.0), 3),
    )


def are_equivalent(a: UniversalMorphologicalAnalysis, b: UniversalMorphologicalAnalysis) -> Dict:
    shared = sorted(set(a.features) & set(b.features))
    return {
        "equivalent": bool(a.features and b.features and set(a.features) == set(b.features)),
        "shared_features": shared,
        "left": a.to_dict(),
        "right": b.to_dict(),
    }


def detect_language(surface: str) -> Optional[str]:
    if any("\u0600" <= ch <= "\u06ff" for ch in surface):
        return "ug"
    if any(0x10C00 <= ord(ch) <= 0x10C4F for ch in surface):
        return "otk"
    if any("\u0400" <= ch <= "\u04ff" for ch in surface):
        return "kk"
    return None
