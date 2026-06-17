import json
from pathlib import Path

def generate(path, n=1000):
    data = []
    # include the real kit(a)b example first
    data.append({
        'proto_form': '*kitab',
        'gloss': 'book',
        'confidence_score': 0.95,
        'entries': [
            {'language': 'uz', 'word': 'kitob', 'lemma': 'kitob'},
            {'language': 'tr', 'word': 'kitap', 'lemma': 'kitap'},
            {'language': 'az', 'word': 'kitab', 'lemma': 'kitab'},
            {'language': 'kk', 'word': 'кітап', 'lemma': 'кітап'},
            {'language': 'ky', 'word': 'китеп', 'lemma': 'китеп'},
            {'language': 'tk', 'word': 'kitap', 'lemma': 'kitap'}
        ]
    })
    for i in range(2, n+1):
        proto = f'*proto_{i:04d}'
        entries = [
            {'language': 'uz', 'word': f'uz_{i}', 'lemma': f'uz_{i}'},
            {'language': 'tr', 'word': f'tr_{i}', 'lemma': f'tr_{i}'},
            {'language': 'az', 'word': f'az_{i}', 'lemma': f'az_{i}'},
            {'language': 'kk', 'word': f'kk_{i}', 'lemma': f'kk_{i}'},
            {'language': 'ky', 'word': f'ky_{i}', 'lemma': f'ky_{i}'},
            {'language': 'tk', 'word': f'tk_{i}', 'lemma': f'tk_{i}'}
        ]
        data.append({'proto_form': proto, 'gloss': f'gloss_{i}', 'confidence_score': 0.8, 'entries': entries})

    p = Path(path) / 'cognates.json'
    with p.open('w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    generate(Path(__file__).parent, n=1000)
