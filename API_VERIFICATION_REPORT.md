# API Verification Report

## POST /api/auth/register/

- status_code: 201

- response sample:

```json

{
  "id": 1,
  "email": "test+api@example.com",
  "first_name": "API",
  "last_name": "Tester",
  "role": "RESEARCHER"
}

```

## POST /api/auth/login/

- status_code: 200

- response sample:

```json

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTM1MDUzMCwiaWF0IjoxNzgwNzQ1NzMwLCJqdGkiOiJhZDQ5NzUyOTFkMzY0YmQwYmY1NjczMjUzMjNmMzU0ZSIsInVzZXJfaWQiOjEsImVtYWlsIjoidGVzdCthcGlAZXhhbXBsZS5jb20iLCJyb2xlIjoiUkVTRUFSQ0hFUiJ9.pyMeYIIYLcvOQG6wnPLwVAStd8qN5cXDR2wsLn-wrRU",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNzQ3NTMwLCJpYXQiOjE3ODA3NDU3MzAsImp0aSI6IjgzODcwMDZkNWFhNTQ1ZGJiNTM2NTU5YmJhMTkyMTUzIiwidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0K2FwaUBleGFtcGxlLmNvbSIsInJvbGUiOiJSRVNFQVJDSEVSIn0.rgFegU72e3YjxaFVpmib5BbOIlU-bFTIyGeM3hzlKb8"
}

```

## POST /api/auth/refresh/

- status_code: 200

- response sample:

```json

{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNzQ3NTMwLCJpYXQiOjE3ODA3NDU3MzAsImp0aSI6IjIwY2JlY2Q1MWU1ZjQ4MGE5MDJmZWQ4MjYxOGU1ODk2IiwidXNlcl9pZCI6MSwiZW1haWwiOiJ0ZXN0K2FwaUBleGFtcGxlLmNvbSIsInJvbGUiOiJSRVNFQVJDSEVSIn0.SDCZ_Lvs-OOX2-W48eZHHA9Y-YqN4b7ZuVa04yHQe_4"
}

```

## GET /api/auth/profile/

- status_code: 200

- response sample:

```json

{
  "id": "26964e4a-fd1b-4506-9c91-7b76dbe40682",
  "user": {
    "id": 1,
    "email": "test+api@example.com",
    "first_name": "API",
    "last_name": "Tester",
    "role": "RESEARCHER"
  },
  "institution": "",
  "research_area": "",
  "bio": "",
  "created_at": "2026-06-06T11:35:29.694092Z",
  "updated_at": "2026-06-06T11:35:29.694092Z"
}

```

## GET /api/languages/

- status_code: 200

- response sample:

```json

{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}

```

## GET /api/languages/statistics/

- status_code: 200

- response sample:

```json

{
  "total_languages": 0,
  "families": [],
  "countries": []
}

```

## GET /api/words/

- status_code: 200

- response sample:

```json

{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}

```

## GET /api/words/search/?q=test

- status_code: 200

- response sample:

```json

{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}

```

## GET /api/words/statistics/

- status_code: 200

- response sample:

```json

{
  "total_words": 0,
  "languages": [],
  "parts_of_speech": [],
  "sources": []
}

```

## GET /api/words/quality/

- status_code: 200

- response sample:

```json

{
  "languages": {
    "uz": {
      "language": "uzbek",
      "total": 10000,
      "valid": 10000,
      "invalid": 0
    },
    "tr": {
      "language": "turkish",
      "total": 10000,
      "valid": 9486,
      "invalid": 514
    },
    "kk": {
      "language": "kazakh",
      "total": 8000,
      "valid": 7997,
      "invalid": 3
    },
    "ky": {
      "language": "kyrgyz",
      "total": 8000,
      "valid": 8000,
      "invalid": 0
    },
    "az": {
      "language": "azerbaijani",
      "total": 8000,
      "valid": 7594,
      "invalid": 406
    },
    "tk": {
      "language": "turkmen",
      "total": 8000,
      "valid": 7579,
      "invalid": 421
    },
    "otk": {
      "language": "old_turkic",
      "total": 8000,
      "valid": 7835,
      "invalid": 165
    }
  },
  "records": {
    "uz": 10000,
    "tr": 10000,
    "kk": 8000,
    "ky": 8000,
    "az": 8000,
    "tk": 8000,
    "otk": 8000
  },
  "duplicates": {
    "uz": 0,
    "tr": 0,
    "kk": 0,
    "ky": 0,
    "az": 0,
    "tk": 0,
    "otk": 0
  },
  "validation_score": {
    "uz": 100.0,
    "tr": 94.86,
    "kk": 99.96,
    "ky": 100.0,
    "az": 94.92,
    "tk": 94.74,
    "otk": 97.94
  }
}

```

## GET /api/corpus/statistics/

- status_code: 200

- response sample:

```json

{
  "documents": 0,
  "sentences": 0,
  "tokens": 0,
  "languages": {}
}

```

## GET /api/cognates/

- status_code: 200

- response sample:

```json

{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}

```

## GET /api/cognates/search/?word=test

- status_code: 200

- response sample:

```json

[]

```

## GET /api/cognates/statistics/

- status_code: 200

- response sample:

```json

{
  "cognate_sets": 0,
  "entries": 0,
  "languages": {}
}

```

## GET /api/admin/languages/ (no auth)

- status_code: 401

- response sample:

```json

{
  "detail": "Authentication credentials were not provided."
}

```

## GET /api/admin/words/ (no auth)

- status_code: 401

- response sample:

```json

{
  "detail": "Authentication credentials were not provided."
}

```

## GET /api/admin/languages/ (researcher)

- status_code: 403

- response sample:

```json

{
  "detail": "You do not have permission to perform this action."
}

```

## GET /api/admin/words/ (researcher)

- status_code: 403

- response sample:

```json

{
  "detail": "You do not have permission to perform this action."
}

```

## Pagination /api/words/ page=1 first call

- status_code: 200

- response sample:

```json

{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}

```

## Pagination /api/words/ page=1 second call

- status_code: 200

- response sample:

```json

{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}

```

## Filter /api/languages/?code=xx

- status_code: 200

- response sample:

```json

{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}

```

## Caching /api/languages/ identical responses

- status_code: 200

- response sample:

```json

{
  "identical": true
}

```

## OpenAPI file exists

- status_code: 200

- response sample:

```json

"backend/openapi_generated.yaml"

```
