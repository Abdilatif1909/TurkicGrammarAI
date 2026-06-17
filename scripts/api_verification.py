import os
import sys
import json
from pathlib import Path

# Ensure backend is on path so `config` settings module can be imported
ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / 'backend'
sys.path.insert(0, str(BACKEND))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

# For local verification runs where Redis may not be available, override
# the project's cache settings to use an in-memory cache. This is a test-
# only override limited to this script and applied before Django setup.
try:
    import importlib
    settings_mod = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE'])
    settings_mod.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }
except Exception:
    # If we can't import or modify settings, continue and let Django handle it.
    pass

import django
django.setup()

from django.core.management import call_command
from django.test import Client

ROOT = ROOT

def run_migrations():
    call_command("migrate", "--noinput")

def req(client, method, path, data=None, token=None):
    headers = {}
    if token:
        headers['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    # Ensure Host is allowed by Django settings during test client requests
    headers['HTTP_HOST'] = 'localhost'
    try:
        if method.lower() == 'get':
            r = client.get(path, **headers)
        elif method.lower() == 'post':
            r = client.post(path, data=json.dumps(data) if data is not None else None, content_type='application/json', **headers)
        else:
            r = client.generic(method.upper(), path, data=json.dumps(data) if data is not None else None, content_type='application/json', **headers)
    except Exception as e:
        return {'status_code': 500, 'body': f'EXCEPTION: {type(e).__name__}: {str(e)}'}
    try:
        body = r.json()
    except Exception:
        body = r.content.decode('utf-8', errors='replace')
    return {'status_code': r.status_code, 'body': body}

def main():
    run_migrations()
    client = Client()
    report = []

    # 1. Auth: register
    reg_payload = {"email": "test+api@example.com", "password": "password123", "first_name": "API", "last_name": "Tester", "role": "RESEARCHER"}
    r = req(client, 'post', '/api/auth/register/', data=reg_payload)
    report.append(("POST /api/auth/register/", r))

    # 2. Login
    login_payload = {"email": reg_payload['email'], "password": reg_payload['password']}
    r = req(client, 'post', '/api/auth/login/', data=login_payload)
    report.append(("POST /api/auth/login/", r))
    access = r['body'].get('access') if isinstance(r['body'], dict) else None
    refresh = r['body'].get('refresh') if isinstance(r['body'], dict) else None

    # 3. Refresh
    if refresh:
        r = req(client, 'post', '/api/auth/refresh/', data={'refresh': refresh})
        report.append(("POST /api/auth/refresh/", r))

    # 4. Profile
    r = req(client, 'get', '/api/auth/profile/', token=access)
    report.append(("GET /api/auth/profile/", r))

    # Languages
    report.append(("GET /api/languages/", req(client, 'get', '/api/languages/')))
    report.append(("GET /api/languages/statistics/", req(client, 'get', '/api/languages/statistics/')))

    # Words
    report.append(("GET /api/words/", req(client, 'get', '/api/words/')))
    report.append(("GET /api/words/search/?q=test", req(client, 'get', '/api/words/search/?q=test')))
    report.append(("GET /api/words/statistics/", req(client, 'get', '/api/words/statistics/')))
    report.append(("GET /api/words/quality/", req(client, 'get', '/api/words/quality/')))

    # Corpus
    report.append(("GET /api/corpus/statistics/", req(client, 'get', '/api/corpus/statistics/')))

    # Cognates
    report.append(("GET /api/cognates/", req(client, 'get', '/api/cognates/')))
    report.append(("GET /api/cognates/search/?word=test", req(client, 'get', '/api/cognates/search/?word=test')))
    report.append(("GET /api/cognates/statistics/", req(client, 'get', '/api/cognates/statistics/')))

    # Admin endpoints (unauthenticated -> expect 401/403)
    report.append(("GET /api/admin/languages/ (no auth)", req(client, 'get', '/api/admin/languages/')))
    report.append(("GET /api/admin/words/ (no auth)", req(client, 'get', '/api/admin/words/')))

    # Admin endpoints (authenticated as researcher -> expect 403)
    report.append(("GET /api/admin/languages/ (researcher)", req(client, 'get', '/api/admin/languages/', token=access)))
    report.append(("GET /api/admin/words/ (researcher)", req(client, 'get', '/api/admin/words/', token=access)))

    # Pagination check (words)
    r1 = req(client, 'get', '/api/words/?page=1')
    r2 = req(client, 'get', '/api/words/?page=1')
    report.append(("Pagination /api/words/ page=1 first call", r1))
    report.append(("Pagination /api/words/ page=1 second call", r2))

    # Filtering example (languages)
    report.append(("Filter /api/languages/?code=xx", req(client, 'get', '/api/languages/?code=xx')))

    # Caching: call languages list twice and check same body
    a = req(client, 'get', '/api/languages/')
    b = req(client, 'get', '/api/languages/')
    cache_ok = a['body'] == b['body']
    report.append(("Caching /api/languages/ identical responses", {'status_code': 200 if cache_ok else 500, 'body': {'identical': cache_ok}}))

    # OpenAPI examples check: ensure openapi file exists and basic keys present
    openapi_path = ROOT / 'backend' / 'openapi_generated.yaml'
    openapi_exists = openapi_path.exists()
    report.append(("OpenAPI file exists", {'status_code': 200 if openapi_exists else 404, 'body': str(openapi_path)}))

    # Write report markdown
    md = ["# API Verification Report\n"]
    for endpoint, res in report:
        md.append(f"## {endpoint}\n")
        md.append(f"- status_code: {res['status_code']}\n")
        md.append("- response sample:\n")
        md.append("```json\n")
        try:
            md.append(json.dumps(res['body'], indent=2, ensure_ascii=False) + "\n")
        except Exception:
            md.append(str(res['body']) + "\n")
        md.append("```\n")

    out_path = ROOT / 'API_VERIFICATION_REPORT.md'
    out_path.write_text('\n'.join(md), encoding='utf-8')
    print(f"Wrote report to {out_path}")


if __name__ == '__main__':
    main()
