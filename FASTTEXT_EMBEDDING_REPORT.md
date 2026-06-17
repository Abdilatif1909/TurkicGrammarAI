# FastText Embedding Report

## Training

- Model: `backend\models\turkic_fasttext.model`
- Vocabulary size: 90825
- Vector size: 300
- Window: 5
- Min count: 1
- Epochs: 20
- Workers: 12
- Training time: 43.113 seconds

## Similarity Examples

### cognate_similarity

| Word A | Word B | Similarity |
| --- | --- | ---: |
| tangri | tanrı | 0.94462 |
| tangri | тәңір | 0.696357 |
| tangri | تەڭرى | 0.617625 |
| kitob | kitap | 0.824031 |
| til | dil | 0.556541 |

### cross_language_similarity

| Word A | Word B | Similarity |
| --- | --- | ---: |
| lang_uz | lang_tr | 0.05311 |
| lang_kk | lang_ky | 0.57264 |
| lang_ug | lang_otk | 0.296245 |

### morphology_similarity

| Word A | Word B | Similarity |
| --- | --- | ---: |
| feat_PLURAL | lar | 0.79097 |
| feat_DERIVATIONAL | chi | 0.621586 |
| feat_DATIVE | ga | 0.566965 |
| feat_ABLATIVE | dan | 0.708296 |

## Nearest Neighbors

### `tangri`

| Neighbor | Score |
| --- | ---: |
| taomi | 0.967514 |
| taom | 0.949418 |
| tanrı | 0.94462 |
| tajriba | 0.943596 |
| taňry | 0.925913 |
| talabaning | 0.898093 |
| tartib | 0.894693 |
| tarixdor | 0.887681 |
| tadbiri | 0.887235 |
| tarixnia | 0.887122 |

### `tanrı`

| Neighbor | Score |
| --- | ---: |
| taňry | 0.985474 |
| taom | 0.967203 |
| taomi | 0.956174 |
| tajriba | 0.955284 |
| tangri | 0.94462 |
| tağči | 0.930372 |
| taği | 0.929749 |
| tağüŋ | 0.924496 |
| tağim | 0.923904 |
| tağçı | 0.923119 |

### `تەڭرى`

| Neighbor | Score |
| --- | ---: |
| ئۈچ | 0.970148 |
| كىشى | 0.965043 |
| كۆك | 0.961467 |
| بەرما | 0.95971 |
| كۆرما | 0.958484 |
| تۇرچى | 0.954818 |
| قارا | 0.954726 |
| ياپما | 0.953789 |
| كەلدى | 0.952741 |
| كەلما | 0.952552 |

### `kitob`

| Neighbor | Score |
| --- | ---: |
| kitobxon | 0.988443 |
| kitobnew | 0.988299 |
| kitobsa | 0.98746 |
| kitobim | 0.987279 |
| kitoba | 0.985993 |
| kitobqa | 0.985825 |
| kitobta | 0.985688 |
| kitobuv | 0.985624 |
| kitobi | 0.98504 |
| kitobxoni | 0.983766 |

### `feat_PLURAL`

| Neighbor | Score |
| --- | ---: |
| sutlarmaamaler | 0.820567 |
| oturluolelar | 0.805533 |
| metrolar | 0.800515 |
| sesler | 0.800338 |
| səssızolaler | 0.79557 |
| ylymsunlar | 0.794091 |
| yıllar | 0.792711 |
| akşamlar | 0.791571 |
| tünuylar | 0.791393 |
| gyşlar | 0.790909 |

### `lang_uz`

| Neighbor | Score |
| --- | ---: |
| rang | 0.781534 |
| davoingiya | 0.778469 |
| xizmatvor | 0.772786 |
| ta'limdor | 0.771919 |
| uyadiroqchi | 0.771439 |
| pulvor | 0.770667 |
| matematikavor | 0.770534 |
| shifoxonaingiya | 0.770419 |
| xizmatkor | 0.769358 |
| madaniyatishvor | 0.766862 |

## Readiness

The FastText baseline is trained and saved. It is ready to compare against a Word2Vec baseline.
