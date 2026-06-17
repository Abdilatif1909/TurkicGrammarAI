from dataclasses import dataclass
from pathlib import Path

from django.conf import settings

from .base_generator import BaseDatasetGenerator


DEFAULT_WORD_TARGETS = {
    "uz": 10000,
    "tr": 10000,
    "kk": 8000,
    "ky": 8000,
    "az": 8000,
    "tk": 8000,
    "otk": 8000,
}

LANGUAGE_FILES = {
    "uz": "uzbek_words.json",
    "tr": "turkish_words.json",
    "kk": "kazakh_words.json",
    "ky": "kyrgyz_words.json",
    "az": "azerbaijani_words.json",
    "tk": "turkmen_words.json",
    "otk": "old_turkic_words.json",
}


@dataclass(frozen=True)
class LanguageGenerationProfile:
    code: str
    roots: tuple[str, ...]
    nominal_suffixes: tuple[str, ...]
    verbal_suffixes: tuple[str, ...]
    adjective_suffixes: tuple[str, ...]
    ipa_map: dict[str, str]


class WordDatasetGenerator(BaseDatasetGenerator):
    source_name = "synthetic-comparative-generator-v1"
    meanings = (
        "body and human life",
        "movement and direction",
        "natural environment",
        "family and society",
        "material culture",
        "time and aspect",
        "quality and state",
        "speech and cognition",
    )
    pos_cycle = ("NOUN", "VERB", "ADJECTIVE", "ADVERB")

    profiles = {
        "uz": LanguageGenerationProfile(
            code="uz",
            roots=("bor", "kel", "bil", "ko'r", "yoz", "o'q", "ish", "bosh", "ko'z", "tog'", "suv", "til"),
            nominal_suffixes=("lar", "imiz", "ning", "dan", "ga", "da", "lik", "chi"),
            verbal_suffixes=("di", "gan", "moqda", "adi", "sa", "ish", "ar", "uvchi"),
            adjective_suffixes=("li", "siz", "chan", "roq", "gi", "iy"),
            ipa_map={"o'": "o", "g'": "ɣ", "sh": "ʃ", "ch": "tʃ"},
        ),
        "tr": LanguageGenerationProfile(
            code="tr",
            roots=("gel", "git", "bil", "gör", "yaz", "oku", "iş", "baş", "göz", "dağ", "su", "dil"),
            nominal_suffixes=("lar", "imiz", "in", "den", "e", "de", "lik", "ci"),
            verbal_suffixes=("di", "miş", "iyor", "er", "se", "mek", "ir", "en"),
            adjective_suffixes=("li", "siz", "ci", "ce", "sel", "imsi"),
            ipa_map={"ş": "ʃ", "ç": "tʃ", "ğ": "ɣ", "ö": "ø", "ü": "y", "ı": "ɯ"},
        ),
        "kk": LanguageGenerationProfile(
            code="kk",
            roots=("bar", "kel", "bil", "kör", "jaz", "oqı", "is", "bas", "köz", "tau", "su", "til"),
            nominal_suffixes=("lar", "imiz", "dıñ", "dan", "ğa", "da", "lıq", "şı"),
            verbal_suffixes=("dı", "ğan", "ıp", "adı", "sa", "w", "ar", "atın"),
            adjective_suffixes=("lı", "sız", "şıl", "law", "ğı", "lıq"),
            ipa_map={"ö": "ø", "ı": "ɯ", "ğ": "ʁ", "ş": "ʃ"},
        ),
        "ky": LanguageGenerationProfile(
            code="ky",
            roots=("bar", "kel", "bil", "kör", "jaz", "oku", "iş", "baş", "köz", "too", "suu", "til"),
            nominal_suffixes=("lar", "ibiz", "dyn", "dan", "ga", "da", "lyk", "chy"),
            verbal_suffixes=("dy", "gan", "yp", "at", "sa", "uu", "ar", "gan"),
            adjective_suffixes=("luu", "syz", "chan", "raak", "ky", "lyk"),
            ipa_map={"ö": "ø", "ş": "ʃ", "ch": "tʃ", "y": "ɯ"},
        ),
        "az": LanguageGenerationProfile(
            code="az",
            roots=("get", "gəl", "bil", "gör", "yaz", "oxu", "iş", "baş", "göz", "dağ", "su", "dil"),
            nominal_suffixes=("lar", "imiz", "ın", "dan", "a", "da", "lıq", "çı"),
            verbal_suffixes=("di", "miş", "ır", "ar", "sa", "maq", "ər", "ən"),
            adjective_suffixes=("lı", "sız", "çı", "ca", "i", "vari"),
            ipa_map={"ə": "æ", "ş": "ʃ", "ç": "tʃ", "ğ": "ɣ", "ö": "ø", "ü": "y"},
        ),
        "tk": LanguageGenerationProfile(
            code="tk",
            roots=("git", "gel", "bil", "gör", "ýaz", "oka", "iş", "baş", "göz", "dag", "suw", "dil"),
            nominal_suffixes=("lar", "imiz", "iň", "dan", "a", "da", "lyk", "çy"),
            verbal_suffixes=("di", "en", "ýär", "ar", "sa", "mak", "er", "ýän"),
            adjective_suffixes=("ly", "syz", "çy", "rak", "ky", "lyk"),
            ipa_map={"ý": "j", "ş": "ʃ", "ç": "tʃ", "ň": "ŋ", "ö": "ø", "ü": "y"},
        ),
        "otk": LanguageGenerationProfile(
            code="otk",
            roots=("bar", "kel", "bil", "kör", "bit", "okı", "iş", "baş", "köz", "tag", "sub", "til"),
            nominal_suffixes=("lar", "imiz", "ıŋ", "dın", "ka", "ta", "lıg", "çı"),
            verbal_suffixes=("dı", "miş", "ur", "ar", "sar", "mak", "ir", "gü"),
            adjective_suffixes=("lıg", "sız", "çı", "rak", "ki", "teg"),
            ipa_map={"ö": "ø", "ı": "ɯ", "ŋ": "ŋ", "ş": "ʃ"},
        ),
    }

    def __init__(self, output_dir: str | Path | None = None, seed: int = 42):
        super().__init__(output_dir or settings.BASE_DIR / "data" / "words", seed=seed)

    def generate(self, targets: dict[str, int] | None = None) -> dict[str, int]:
        targets = targets or DEFAULT_WORD_TARGETS
        summary = {}
        for language_code, count in targets.items():
            records = self.generate_language(language_code, count)
            self.write_json(LANGUAGE_FILES[language_code], records)
            summary[LANGUAGE_FILES[language_code]] = len(records)
        return summary

    def generate_language(self, language_code: str, count: int) -> list[dict]:
        profile = self.profiles[language_code]
        records = []
        seen = set()
        index = 0
        while len(records) < count:
            root = profile.roots[index % len(profile.roots)]
            pos = self.pos_cycle[index % len(self.pos_cycle)]
            suffix = self._suffix_for_pos(profile, pos, index)
            word = self._compose_word(profile, root, suffix, pos, index)
            lemma = root
            meaning = f"{self.meanings[index % len(self.meanings)]}; generated lexical item {len(records) + 1}"
            key = (word, lemma, pos, meaning)
            if key in seen:
                index += 1
                continue
            seen.add(key)
            records.append(
                {
                    "language_code": language_code,
                    "word": word,
                    "lemma": lemma,
                    "root": root,
                    "pos": pos,
                    "ipa": self._to_ipa(word, profile.ipa_map),
                    "meaning": meaning,
                    "frequency": self._frequency(index),
                    "source": self.source_name,
                    "notes": f"Generated from root '{root}' with suffix '{suffix}'.",
                }
            )
            index += 1
        return records

    @staticmethod
    def _suffix_for_pos(profile: LanguageGenerationProfile, pos: str, index: int) -> str:
        if pos == "VERB":
            suffixes = profile.verbal_suffixes
        elif pos == "ADJECTIVE":
            suffixes = profile.adjective_suffixes
        elif pos == "ADVERB":
            suffixes = profile.adjective_suffixes + profile.nominal_suffixes
        else:
            suffixes = profile.nominal_suffixes
        return suffixes[(index // len(profile.roots)) % len(suffixes)]

    @staticmethod
    def _compose_word(profile: LanguageGenerationProfile, root: str, suffix: str, pos: str, index: int) -> str:
        suffix_layers = profile.nominal_suffixes + profile.verbal_suffixes + profile.adjective_suffixes
        second_suffix = suffix_layers[(index // 31) % len(suffix_layers)]
        partner_root = profile.roots[(index // 211) % len(profile.roots)]
        if index % 7 == 0:
            return f"{root}{partner_root}{suffix}"
        if index % 5 == 0:
            return f"{root}{suffix}{second_suffix}"
        if pos == "ADVERB":
            return f"{root}{suffix}{second_suffix}"
        return f"{root}{suffix}"

    @staticmethod
    def _frequency(index: int) -> int:
        return max(1, 100000 // (index + 25))

    @staticmethod
    def _to_ipa(word: str, ipa_map: dict[str, str]) -> str:
        ipa = word
        for source, target in sorted(ipa_map.items(), key=lambda item: len(item[0]), reverse=True):
            ipa = ipa.replace(source, target)
        return ipa.replace("'", "").replace("q", "q").replace("x", "χ")
