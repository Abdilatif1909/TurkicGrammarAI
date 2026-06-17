# Uzbek Morphology Error Report

Total benchmark cases: 500
Total failures: 385

## Error type counts

| Error Type | Count |
| ---------- | -----:|
| ROOT_ERROR | 186 |
| RULE_MISSING | 117 |
| SCORING_ERROR | 82 |

## Top 50 failure patterns

- chi -> i — 5
- iyimiz -> iy|imiz — 3
- moqdadan -> da|dan — 2
- ning -> ing — 2
- ganmai -> gan|ma|i — 2
- qaingiz -> qa|ingiz — 2
- taish -> ish — 2
- larida -> lari|da — 2
- yorari -> yor|ar|i — 2
- chauv -> cha|uv — 2
- imo' -> im|o' — 2
- maadi -> i — 2
- damoqda -> da — 2
- yoruv -> yor|uv — 2
- yoro'i -> yor|o'|i — 2
- uvdeni|ingish -> ni|ing|ish — 1
- lariyor|o' -> lari|yor|o' — 1
- qaimiz|ishvor|taara -> qa|imiz|ish|vor|taara — 1
- cha|dichi -> i — 1
- diga -> i|ga — 1
- adinii|tadan -> dan — 1
- dan|ingyor -> dan|ing|yor — 1
- adini|iyma -> i|iy|ma — 1
- maganden -> magan|den — 1
- diringiz -> dir|ingiz — 1
- o'|gindaa|maler -> o'|gindaa|ma|ler — 1
- ning|adi -> i — 1
- data|deni -> ni — 1
- malara|ar|ler -> or|malara|ar|ler — 1
- yorning -> ing — 1
- tamagan -> magan — 1
- machii|ginacha -> i|i|ginacha — 1
- ganlar|yoro'i -> ar|yor|o'|i — 1
- iyga -> iy|ga — 1
- lik|masaa|imdaa -> or|lik|masaa|imdaa — 1
- im|leryor|o'ta -> im|ler|yor|o'ta — 1
- niingiz -> i|ingiz — 1
- chaqa -> cha|qa — 1
- taish|gina|uvchi -> i — 1
- data|o'roqi|lerning -> ing — 1
- argini|qaingiz|gingaa -> argini|qa|ingiz|gingaa — 1
- ga|masai -> ga|ma|sa|i — 1
- ingizim -> ingiz|im — 1
- ari -> im|ar|i — 1
- maganler -> magan|ler — 1
- ilari|roqmoqda -> da — 1
- dir|ishning -> ing — 1
- liklar|iyma|o'ta -> ar|iy|ma|o'ta — 1
- o'moqda|uvdeni -> ni — 1
- leryor|yor -> ler|yor|yor — 1

## Most frequent suffix conflicts

- ['chi'] -> ['i'] : 5
- ['iyimiz'] -> ['iy', 'imiz'] : 3
- ['moqdadan'] -> ['da', 'dan'] : 2
- ['ning'] -> ['ing'] : 2
- ['ganmai'] -> ['gan', 'ma', 'i'] : 2
- ['qaingiz'] -> ['qa', 'ingiz'] : 2
- ['taish'] -> ['ish'] : 2
- ['larida'] -> ['lari', 'da'] : 2
- ['yorari'] -> ['yor', 'ar', 'i'] : 2
- ['chauv'] -> ['cha', 'uv'] : 2
- ["imo'"] -> ['im', "o'"] : 2
- ['maadi'] -> ['i'] : 2
- ['damoqda'] -> ['da'] : 2
- ['yoruv'] -> ['yor', 'uv'] : 2
- ["yoro'i"] -> ['yor', "o'", 'i'] : 2
- ['uvdeni', 'ingish'] -> ['ni', 'ing', 'ish'] : 1
- ['lariyor', "o'"] -> ['lari', 'yor', "o'"] : 1
- ['qaimiz', 'ishvor', 'taara'] -> ['qa', 'imiz', 'ish', 'vor', 'taara'] : 1
- ['cha', 'dichi'] -> ['i'] : 1
- ['diga'] -> ['i', 'ga'] : 1

## Most frequent root conflicts

- ta'lim -> ta'l : 18
- bozor -> boz : 16
- daryo -> daryota : 4
- daryo -> daryoch : 3
- yurak -> yurakn : 3
- oila -> oilayoruvch : 2
- til -> tiln : 2
- ish -> ishn : 2
- o'q -> o'qch : 2
- oila -> oilalikl : 2
- daryo -> daryouvde : 1
- daryo -> daryochadich : 1
- o'q -> o'qd : 1
- ish -> ishadiniita : 1
- o'q -> o'qadin : 1
- daryo -> daryoningad : 1
- bozor -> bozordatade : 1
- ish -> ishyorn : 1
- ta'lim -> ta'limmach : 1
- yoz -> yozganl : 1

## Recommendations (automated analysis)

- Review RULE_MISSING cases to add missing suffix rules.
- For SCORING_ERROR cases, inspect scoring for the expected sequence.
- For AMBIGUITY_ERROR cases, consider stronger lexical entries or curated full-word entries.
