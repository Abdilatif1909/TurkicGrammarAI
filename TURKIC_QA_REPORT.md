# Turkic QA Report

## Pipeline

Question -> RAG Retrieval -> Top-K Results -> Structured Answer Builder -> Response with citations.

## Evaluation

| Metric | Value |
| --- | ---: |
| Questions | 1000 |
| Answer Accuracy | 83.8% |
| Source Accuracy | 99.7% |
| Top-K Support Coverage | 83.8% |

## Category Metrics

| Category | Questions | Answer Accuracy | Source Accuracy | Top-K Support |
| --- | ---: | ---: | ---: | ---: |
| cognate | 250 | 89.2% | 99.6% | 89.2% |
| cross-language | 250 | 77.2% | 100.0% | 77.2% |
| historical | 250 | 100.0% | 100.0% | 100.0% |
| morphology | 250 | 68.8% | 99.2% | 68.8% |

## Top Successful Cases

- tangri so'zining turkiy tillardagi shakllari qanday? -> ['теңир', 'تەڭرى', 'taňry', '𐱅𐰭𐰼𐰃', 'tanrı', 'тәңір'].
- kitob so'zining turkiy tillardagi shakllari qanday? -> ['kitap', 'kitab'].
- uy so'zining turkiy tillardagi shakllari qanday? -> ['ئۆي', 'öý', 'ev', '𐰋', 'үй'].
- kishi so'zining turkiy tillardagi shakllari qanday? -> ['киши', 'كىشى', 'кісі', 'kişi'].
- ota so'zining turkiy tillardagi shakllari qanday? -> ['ata', 'ئاتا', '𐰀𐱃𐰀'].
- ona so'zining turkiy tillardagi shakllari qanday? -> ['эне', '𐰀𐰣𐰀', 'ئانا', 'ana', 'ана'].
- suv so'zining turkiy tillardagi shakllari qanday? -> ['سۇ', 'su', 'су', 'suw', 'суу', '𐰽𐰆'].
- tosh so'zining turkiy tillardagi shakllari qanday? -> ['таш', 'тас', 'daş', 'taş', 'تاش', '𐱃𐰀𐱁'].
- yo‘l so'zining turkiy tillardagi shakllari qanday? -> ['жол', 'يول', '𐰖𐰆𐰞', 'yol'].
- bir so'zining turkiy tillardagi shakllari qanday? -> ['𐰋𐰃𐰼', 'бір', 'بىر', 'бир'].

## Top Failed Cases

- til so'zining turkiy tillardagi shakllari qanday?: expected ['dil', 'тіл', 'тил', 'تىل', '𐱅𐰃𐰠'], returned ['til', 'til', 'tiltil', 'tilči', 'tiluŋ'].
- maktab so'zining turkiy tillardagi shakllari qanday?: expected ['masa', 'кітаплі', 'китепсиз', 'kitapsiz', 'ئۆيچى'], returned ['maktab', 'maktabi', 'maktabmaktabni', 'maktabmaktabga', 'maktabmaktabda'].
- xalq so'zining turkiy tillardagi shakllari qanday?: expected ['yemek', 'yemək', 'қалады', 'адамдөш', 'mekdepsiz'], returned ['xalq', 'xalq', 'xalqə', 'xalqxalqə', 'xalqü'].
- shahar so'zining turkiy tillardagi shakllari qanday?: expected ['para', 'pul', 'қалалы', 'шаарчы', 'Ã§aga'], returned ['shahar', 'sunshahar', 'shaharxon', 'shaharnewi', 'shaharim'].
- qishloq so'zining turkiy tillardagi shakllari qanday?: expected ['pazar', 'bazar', 'қалалі', 'шаарчи', 'Ã§agaçy'], returned ['qishloq', 'qishloqi', 'qishloqga', 'qishloqim', 'qishloqxon'].
- program so'zining turkiy tillardagi shakllari qanday?: expected ['proqram', 'мектепшы', 'шаарлүк', 'Ã§agaly', 'سۆزلىق'], returned ['program', 'programun', 'programe', 'programuy', 'programu'].
- universitet so'zining turkiy tillardagi shakllari qanday?: expected ['sağlık', 'sağlamlıq', 'балалық', 'балалүк', 'yolsiz'], returned ['universitet', 'universitet', 'universitetu', 'universitetü', 'universitetə'].
- tilim so'zining turkiy tillardagi shakllari qanday?: expected ['yazar', 'баладі', 'баласуз', 'obaçy', 'ئەلسىز'], returned ['tilim', 'tilim', 'tiltilim', 'uytilim', 'ishtilim'].
- oila a'zos so'zining turkiy tillardagi shakllari qanday?: expected ['al', 'жолді', 'айылсыз', 'dagçi', 'گۈلچىلىق'], returned ['oila', 'كىتابچى', 'кітапшы', 'китепчы', 'oilaiy'].
- kitobxon so'zining turkiy tillardagi shakllari qanday?: expected ['ara', 'суші', 'жолчы', 'dagdaş', 'ئاتاچىلىق'], returned ['kitobxon', 'kitobkor', 'kitobnewxon', 'kitob', 'kitobsunkor'].

## Source Citation Schema

Every answer item and citation includes `source_type`, `source_id`, and `confidence`.

## Readiness

The retrieval-based QA service is operational and ready for integration with a chatbot or frontend QA surface.
