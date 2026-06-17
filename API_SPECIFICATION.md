# TurkicGrammarAI API Specification

## 1. API Principles

- REST API under `/api/v1/`.
- JSON request and response bodies.
- JWT-style access and refresh token authentication.
- Role-aware permissions on every protected endpoint.
- Long-running NLP tasks return a job id and are processed by Celery.
- List endpoints support pagination, filtering, ordering, and search.

## 2. Authentication

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/register/` | Create student or researcher account request | Public |
| POST | `/api/v1/auth/login/` | Obtain access and refresh tokens | Public |
| POST | `/api/v1/auth/refresh/` | Refresh access token | Authenticated |
| POST | `/api/v1/auth/logout/` | Revoke refresh token | Authenticated |
| GET | `/api/v1/auth/me/` | Current user profile and roles | Authenticated |
| PATCH | `/api/v1/auth/me/` | Update own profile | Authenticated |
| POST | `/api/v1/auth/password/change/` | Change password | Authenticated |
| POST | `/api/v1/auth/password/reset/` | Start password reset | Public |

## 3. Role and User Administration

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/v1/accounts/users/` | List users | Super Admin |
| GET | `/api/v1/accounts/users/{id}/` | Retrieve user | Super Admin |
| PATCH | `/api/v1/accounts/users/{id}/` | Update user status/profile | Super Admin |
| GET | `/api/v1/accounts/roles/` | List roles | Super Admin |
| POST | `/api/v1/accounts/users/{id}/roles/` | Assign role | Super Admin |
| DELETE | `/api/v1/accounts/users/{id}/roles/{role_id}/` | Remove role | Super Admin |
| GET | `/api/v1/accounts/audit-logs/` | View audit logs | Super Admin |

## 4. Languages API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/v1/languages/` | List languages | Authenticated |
| POST | `/api/v1/languages/` | Create language | Super Admin |
| GET | `/api/v1/languages/{id}/` | Retrieve language | Authenticated |
| PATCH | `/api/v1/languages/{id}/` | Update language | Super Admin |
| DELETE | `/api/v1/languages/{id}/` | Archive language | Super Admin |
| GET | `/api/v1/languages/{id}/dialects/` | List dialects | Authenticated |
| GET | `/api/v1/languages/{id}/phonemes/` | List phonemes | Authenticated |
| GET | `/api/v1/languages/{id}/sound-correspondences/` | Compare sound mappings | Researcher, Super Admin |

## 5. Corpus API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/v1/corpus/corpora/` | List visible corpora | Authenticated |
| POST | `/api/v1/corpus/corpora/` | Create corpus | Researcher, Super Admin |
| GET | `/api/v1/corpus/corpora/{id}/` | Retrieve corpus | Object permission |
| PATCH | `/api/v1/corpus/corpora/{id}/` | Update corpus | Owner, Super Admin |
| POST | `/api/v1/corpus/corpora/{id}/documents/` | Upload document | Researcher, Super Admin |
| GET | `/api/v1/corpus/documents/{id}/` | Retrieve document | Object permission |
| POST | `/api/v1/corpus/documents/{id}/index/` | Start indexing job | Owner, Super Admin |
| GET | `/api/v1/corpus/search/` | Search corpus text | Authenticated |
| GET | `/api/v1/corpus/statistics/` | Corpus statistics | Researcher, Super Admin |

## Cognates API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/cognates/` | List cognate sets | Authenticated |
| GET | `/api/cognates/{id}/` | Retrieve cognate set with entries | Authenticated |
| GET | `/api/cognates/search/` | Comparative search by `word` and optional `language` | Authenticated |
| GET | `/api/cognates/statistics/` | Cognates statistics (counts per language) | Authenticated |

Search parameters for `/api/cognates/search/`:

- `word` (required): word to search for
- `language` (optional): language code to restrict search

Example comparative search request:

`GET /api/cognates/search/?word=kitob&language=uz`

Example response:

```json
{
  "proto_form": "*kitab",
  "cognates": [
    {"language":"uz","word":"kitob"},
    {"language":"tr","word":"kitap"},
    {"language":"az","word":"kitab"}
  ]
}
```


### Corpus statistics (actual endpoint in this repo)

The project exposes a corpus statistics endpoint at:

- `GET /api/corpus/statistics/`

Response (200):

```json
{
  "documents": 12345,
  "sentences": 98765,
  "tokens": 543210,
  "languages": {
    "uzbek": 123,
    "turkish": 456,
    "azerbaijani": 78
  }
}
```

Notes:
- The repo-level API path uses `/api/` (no `v1` prefix) for now. The OpenAPI schema includes `/api/corpus/statistics/`.
- Authentication: JWT Bearer token recommended for protected access; read-only access allowed for unauthenticated users depending on permission settings.


## 6. Morphology API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| POST | `/api/v1/morphology/analyze/` | Analyze word or sentence | Authenticated |
| POST | `/api/v1/morphology/batch-analyze/` | Start batch analysis job | Researcher, Super Admin |
| GET | `/api/v1/morphology/lemmas/` | List lemmas | Authenticated |
| POST | `/api/v1/morphology/lemmas/` | Create lemma | Researcher, Super Admin |
| GET | `/api/v1/morphology/affixes/` | List affixes | Authenticated |
| POST | `/api/v1/morphology/affixes/` | Create affix | Researcher, Super Admin |
| GET | `/api/v1/morphology/analyses/{id}/` | Retrieve analysis | Authenticated |

### Morphology

- `GET /api/morphology/analyze/?word={word}&language={lang}` — returns ranked morphological analyses for `word` in `lang`.
- `POST /api/morphology/batch-analyze/` — JSON body: `{ "language": "uz", "words": ["kitoblarimizdan"] }` returning analyses per word.
- `GET /api/morphology/statistics/` — returns counts of morphology rules and stored analyses.

## 7. Cognates API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| POST | `/api/v1/cognates/detect/` | Detect cognate candidates | Researcher, Super Admin |
| POST | `/api/v1/cognates/compare/` | Compare two words or lemmas | Authenticated |
| GET | `/api/v1/cognates/sets/` | List cognate sets | Authenticated |
| POST | `/api/v1/cognates/sets/` | Create curated cognate set | Researcher, Super Admin |
| GET | `/api/v1/cognates/sets/{id}/` | Retrieve cognate set | Authenticated |
| POST | `/api/v1/cognates/sets/{id}/members/` | Add cognate member | Researcher, Super Admin |
| GET | `/api/v1/cognates/pairs/` | List pairwise scores | Researcher, Super Admin |

## 8. Historical Grammar API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/v1/historical/periods/` | List historical periods | Authenticated |
| GET | `/api/v1/historical/forms/` | List historical forms | Authenticated |
| POST | `/api/v1/historical/forms/` | Create historical form | Researcher, Super Admin |
| GET | `/api/v1/historical/proto-forms/` | List proto forms | Authenticated |
| POST | `/api/v1/historical/compare/` | Compare old and modern forms | Authenticated |
| GET | `/api/v1/historical/rules/` | List grammar and sound rules | Authenticated |
| POST | `/api/v1/historical/rules/` | Create rule | Researcher, Super Admin |

## 9. Embeddings API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/v1/embeddings/models/` | List embedding models | Researcher, Super Admin |
| POST | `/api/v1/embeddings/models/` | Register model | Super Admin |
| POST | `/api/v1/embeddings/generate/` | Start embedding job | Researcher, Super Admin |
| POST | `/api/v1/embeddings/similarity/` | Compute semantic similarity | Authenticated |
| GET | `/api/v1/embeddings/spaces/` | List vector spaces | Researcher, Super Admin |
| GET | `/api/v1/embeddings/jobs/{id}/` | Retrieve embedding job status | Owner, Super Admin |

## 10. Chatbot API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/v1/chatbot/sessions/` | List own sessions | Authenticated |
| POST | `/api/v1/chatbot/sessions/` | Create session | Authenticated |
| GET | `/api/v1/chatbot/sessions/{id}/messages/` | List messages | Owner |
| POST | `/api/v1/chatbot/sessions/{id}/messages/` | Ask question | Authenticated |
| GET | `/api/v1/chatbot/messages/{id}/contexts/` | View cited retrieval context | Owner |

## 11. Analytics and Visualization API

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/v1/analytics/overview/` | Platform overview | Super Admin |
| GET | `/api/v1/analytics/corpus/` | Corpus analytics | Researcher, Super Admin |
| GET | `/api/v1/analytics/models/` | Model performance | Researcher, Super Admin |
| GET | `/api/v1/visualization/similarity-matrix/` | Similarity matrix data | Authenticated |
| GET | `/api/v1/visualization/language-tree/` | Language tree data | Authenticated |
| GET | `/api/v1/visualization/embedding-projection/` | 2D or 3D embedding projection | Researcher, Super Admin |
| POST | `/api/v1/visualization/saved-views/` | Save visualization configuration | Authenticated |

## 12. Standard Response Shapes

### Success

```json
{
  "data": {},
  "meta": {
    "request_id": "uuid",
    "timestamp": "2026-06-04T00:00:00Z"
  }
}
```

### Validation Error

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid input.",
    "fields": {}
  }
}
```

### Async Job Response

```json
{
  "data": {
    "job_id": "uuid",
    "status": "queued",
    "status_url": "/api/v1/jobs/{job_id}/"
  }
}
```

## 13. Cross-Cutting Endpoints

| Method | Endpoint | Purpose | Access |
| --- | --- | --- | --- |
| GET | `/api/v1/jobs/{id}/` | Retrieve async job status | Owner, Super Admin |
| POST | `/api/v1/exports/` | Start export job | Researcher, Super Admin |
| GET | `/api/v1/exports/{id}/download/` | Download export | Owner, Super Admin |
