import collections
import json
import sys
from pathlib import Path

default_path = Path(__file__).resolve().parents[1] / "data" / "reports" / "uzbek_morphology_errors.json"
p = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path
with p.open(encoding='utf-8') as fh:
    data = json.load(fh)

types = collections.Counter()
words = collections.Counter()
for e in data:
    types[e.get('type', 'UNKNOWN')] += 1
    words[e.get('word', '')] += 1

print('TYPE_COUNTS')
for k, v in types.most_common():
    print(f'{k}: {v}')

print('\nTOP20_FAILURE_WORDS')
for w, c in words.most_common(20):
    print(f'{w}: {c}')
