import re
from typing import List


TOKEN_RE = re.compile(r"\w+|[^	\w\s]", re.UNICODE)


def tokenize_text(text: str) -> List[str]:
    if not text:
        return []
    tokens = TOKEN_RE.findall(text)
    return tokens
