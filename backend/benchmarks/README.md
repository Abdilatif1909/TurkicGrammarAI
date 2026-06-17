# Word Import Benchmarks

Benchmark command:

```bash
cd backend
python manage.py benchmark_words_import
```

The target is importing 60,000+ generated records in under 120 seconds using `bulk_create`, transactions, duplicate detection, and a default `batch_size` of 5000.
