"""Shared corpus constants: the per-language data sub-directory layout."""

# Language code -> on-disk corpus sub-directory under backend/data/corpus/.
LANGUAGE_DIRECTORIES = {
    "uz": "uzbek",
    "tr": "turkish",
    "az": "azerbaijani",
    "kk": "kazakh",
    "ky": "kyrgyz",
    "tk": "turkmen",
    "otk": "old_turkic",
}

# Reverse lookup: directory name -> language code.
DIRECTORY_LANGUAGES = {directory: code for code, directory in LANGUAGE_DIRECTORIES.items()}

SUPPORTED_FORMATS = ("txt", "json", "csv", "xml")
