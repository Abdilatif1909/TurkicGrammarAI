# Cognates app

This app provides a comparative-historical cognate management system.

Key components:

- `models.py`: `CognateSet`, `CognateEntry`
- `services/`: import, export, comparative search, statistics
- `management/commands/seed_cognates.py`: seed dataset from `backend/data/cognates/cognates.json`
- `views.py` + `urls.py`: list, detail, search, statistics endpoints

Usage:

1. Place `cognates.json` into `backend/data/cognates/`.
2. Run `python manage.py seed_cognates` to populate the DB.

Notes:
- Import command is idempotent and uses transactions and `bulk_create`.
- Avoid training models as part of the import.
