# Contributing

Thank you for your interest in TurkicGrammarAI. The project is currently a research prototype, so contributions should prioritize correctness, reproducibility, and provenance over new features.

## Priority Areas

- Dataset provenance and source metadata.
- Expert review of morphology, cognate, historical, retrieval, and QA records.
- Django API consistency, tests, migrations, and security hardening.
- Frontend tests and accessibility checks.
- Independent benchmark design.
- Documentation and reproducibility.

## Before Opening A Pull Request

1. Keep changes scoped.
2. Do not modify algorithms or evaluation results unless the PR is explicitly about that topic.
3. Do not introduce unsupported scientific claims.
4. Run the relevant checks:

```bash
cd backend
python manage.py check
python manage.py test
```

```bash
cd frontend
npm run build
```

5. Document any dataset or model artifact changes in the relevant manifest.

## Data Contributions

Data contributions should include:

- language code;
- source citation;
- license or reuse status;
- curator/reviewer status;
- whether the item is generated, projected, or expert-reviewed;
- normalization notes for script, transliteration, and Unicode handling.

## Code Style

- Follow existing Django app boundaries and service-layer patterns.
- Keep endpoint behavior aligned with documented `/api/` routes.
- Add tests for permission-sensitive, data-changing, or public API behavior.
- Avoid broad refactors in release-preparation PRs.

## Security

Do not commit secrets, local databases, logs, tokens, private URLs, or credentials. Use `.env.example` and `.env.production.example` only as templates.
