import json
import os

from django.core.management.base import BaseCommand


SEEDS = {
    "Noun -> Profession": {
        "chi": [
            ("ish", "ishchi"),
            ("ma'ruza", "ma'ruzachi"),
            ("bozor", "bozorchi"),
            ("til", "tilchi"),
            ("adabiyot", "adabiyotchi"),
            ("san'at", "san'atchi"),
            ("soliq", "soliqchi"),
            ("matematika", "matematikachi"),
            ("dastur", "dasturchi"),
            ("gaz", "gazchi"),
        ],
        "kor": [
            ("tadbir", "tadbirkor"),
            ("shifo", "shifokor"),
            ("ijod", "ijodkor"),
            ("xizmat", "xizmatkor"),
            ("hunar", "hunarkor"),
        ],
        "gar": [
            ("savdo", "savdogar"),
            ("zar", "zargar"),
            ("mis", "misgar"),
            ("kimyo", "kimyogar"),
            ("hiyla", "hiylagar"),
        ],
    },
    "Verb -> Agent": {
        "uvchi": [
            ("sot", "sotuvchi"),
            ("yoz", "yozuvchi"),
            ("boshqar", "boshqaruvchi"),
            ("qur", "quruvchi"),
            ("ber", "beruvchi"),
            ("ol", "oluvchi"),
            ("kel", "keluvchi"),
            ("bor", "boruvchi"),
            ("tur", "turuvchi"),
            ("ko'r", "ko'ruvchi"),
        ],
        "tuvchi": [
            ("o'qi", "o'qituvchi"),
            ("tani", "tanituvchi"),
            ("boyi", "boyituvchi"),
            ("kengayi", "kengayituvchi"),
            ("qizi", "qizituvchi"),
        ],
    },
    "Verb -> Noun": {
        "ish": [
            ("sot", "sotish"),
            ("yoz", "yozish"),
            ("qur", "qurish"),
            ("bil", "bilish"),
            ("boshqar", "boshqarish"),
            ("kel", "kelish"),
            ("bor", "borish"),
            ("ol", "olish"),
            ("ber", "berish"),
            ("tur", "turish"),
            ("ko'r", "ko'rish"),
        ],
        "uv": [
            ("sot", "sotuv"),
            ("yoz", "yozuv"),
            ("qur", "quruv"),
            ("bor", "boruv"),
            ("kel", "keluv"),
        ],
    },
    "Noun -> Adjective": {
        "li": [
            ("suv", "suvli"),
            ("sut", "sutli"),
            ("madaniyat", "madaniyatli"),
            ("ma'no", "ma'noli"),
            ("kuch", "kuchli"),
            ("aql", "aqlli"),
            ("tartib", "tartibli"),
            ("foyda", "foydali"),
            ("rang", "rangli"),
            ("tajriba", "tajribali"),
        ],
        "siz": [
            ("uy", "uysiz"),
            ("ish", "ishsiz"),
            ("suv", "suvsiz"),
            ("ma'no", "ma'nosiz"),
            ("tartib", "tartibsiz"),
            ("foyda", "foydasiz"),
            ("xato", "xatosiz"),
            ("chegara", "chegarasiz"),
            ("kuch", "kuchsiz"),
            ("tajriba", "tajribasiz"),
        ],
        "dosh": [
            ("sinf", "sinfdosh"),
            ("yo'l", "yo'ldosh"),
            ("fikr", "fikrdosh"),
            ("kurs", "kursdosh"),
            ("mahalla", "mahalladosh"),
        ],
    },
    "Adjective -> Noun": {
        "lik": [
            ("yaxshi", "yaxshilik"),
            ("band", "bandlik"),
            ("do'st", "do'stlik"),
            ("tinch", "tinchlik"),
            ("erkin", "erkinlik"),
            ("go'zal", "go'zallik"),
            ("toza", "tozalik"),
            ("aniq", "aniqlik"),
            ("tez", "tezlik"),
            ("yosh", "yoshlik"),
        ],
    },
}


class Command(BaseCommand):
    help = "Generate a deterministic Uzbek derivational benchmark"

    def add_arguments(self, parser):
        parser.add_argument("--path", help="Path to benchmark dir", default=None)
        parser.add_argument("--count", type=int, default=500)

    def handle(self, *args, **options):
        bench_dir = options.get("path") or os.path.join("backend", "data", "benchmark")
        os.makedirs(bench_dir, exist_ok=True)
        bench_file = os.path.join(bench_dir, "uzbek_derivational_benchmark.json")

        base_cases = []
        for category, by_suffix in SEEDS.items():
            for derivation, pairs in by_suffix.items():
                for root, surface in pairs:
                    base_cases.append({
                        "surface": surface,
                        "expected_root": root,
                        "expected_derivation": derivation,
                        "category": category,
                    })

        count = options.get("count")
        bench = []
        for idx in range(count):
            item = dict(base_cases[idx % len(base_cases)])
            item["id"] = idx + 1
            bench.append(item)

        with open(bench_file, "w", encoding="utf-8") as out:
            json.dump(bench, out, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Wrote {len(bench)} benchmark cases to {bench_file}"))
