$env:USE_SQLITE = "True"
$env:SQLITE_NAME = "db.sqlite3"
$env:DEBUG = "True"
$env:CORS_ALLOWED_ORIGINS = "http://127.0.0.1:5174,http://localhost:5174,http://127.0.0.1:5173,http://localhost:5173"
$env:CORS_ALLOW_ALL_ORIGINS = "True"
python manage.py runserver --noreload 127.0.0.1:8000
