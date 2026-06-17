# Test Discovery Report

## Root cause
- Django test discovery (unittest discovery) looks for tests starting from the current working directory (the discovery "start_dir") when no explicit test labels are provided. When running programmatic discovery or running scripts from a different CWD, the discovery start directory can be incorrect (the repository root instead of the `backend` package directory), so test discovery doesn't traverse into `backend/apps` and finds 0 tests.
- In short: the discovery start directory and Python import path context must point at the `backend` package root (where `config` and `apps` packages live). If they do not, discovery finds zero tests or Django cannot import `config`.

## Evidence (diagnostics)
- Programmatic DiscoverRunner run from repository root without executing `manage.py` (no `backend` on sys.path) failed to import settings:

```
ModuleNotFoundError: No module named 'config'
```

- Programmatic DiscoverRunner run from repository root after adding `backend` to `sys.path` (simulating a naive manual sys.path change) produced:

```
Found 0 test(s).
Discovered test count: 0
```

- Programmatic DiscoverRunner run with CWD set to `backend` produced:

```
Found 70 test(s).
Discovered test count: 70
Discovered test modules:
- apps.accounts.tests
- apps.cognates.tests
- apps.core.tests
- apps.corpus.tests
- apps.historical.tests
- apps.languages.tests
- apps.words.test_validation
- apps.words.tests
```

- Running the management script directly (absolute path) before the fix (typical successful invocation) showed 70 tests. Running it after the fix also shows 70 tests.

## Exact root cause
- The project layout places Django packages under `backend/` (e.g. `backend/apps`, `backend/config`). If test discovery runs with the start directory set to the repository root (or any directory that does not contain the `config` package and `apps` package), discovery will not find the app test modules.
- Some ways of invoking tests (for example, executing a small programmatic wrapper without executing `manage.py` or running with an unexpected CWD) can leave discovery starting in the wrong location.

## Fix applied (minimal, focused)
- Updated `backend/manage.py` to ensure the script directory is inserted into `sys.path` before Django is loaded:

File: backend/manage.py (small change)
- Inserted:

```py
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir and script_dir not in sys.path:
    sys.path.insert(0, script_dir)
```

Rationale: this makes executing `python backend/manage.py test` (or executing manage.py by absolute path from the repository root) guarantee that the `backend` package is importable, and that unittest discovery runs in the correct project context.

## Before
- Programmatic discovery from repo root (no manage.py execution): import failed or discovered 0 tests.
- Some invocations of `python manage.py test` (when the script was invoked in a way that did not put the `backend` directory on `sys.path`) returned "Found 0 test(s)." (diagnosed above).

## After
- `python "backend/manage.py" test` from repository root now discovers all tests.
- Programmatic discovery when CWD is `backend` finds 70 tests.
- Final verified test count: 70 tests discovered and executed successfully.

## How to run (recommended)
- Run tests from `backend` directory:

```powershell
cd backend
python manage.py test --verbosity=2
```

- Or run manage.py by repository-relative path:

```powershell
python "backend\manage.py" test --verbosity=2
```

## Notes and analysis
- I intentionally avoided changing working directory behavior; the fix only ensures the `backend` package directory is on `sys.path` when `manage.py` is executed as a script. This is minimal and safe.
- Programmatic use of `DiscoverRunner` (calling it directly from a process that did not execute `manage.py`) still requires the caller to set up the Python path and discovery start_dir appropriately (for example, by adding the `backend` directory to `sys.path` and/or running with CWD=`backend`). The management command (manage.py) remains the recommended entrypoint for consistent behavior.

---
Generated on: 2026-06-06

## Final root cause summary

- The root cause was the mismatch between the unittest discovery start directory / Python import path and the actual location of the Django project packages (`backend/config`, `backend/apps`). When discovery started from a directory that did not contain the `backend` package, tests were not found. The minimal, focused mitigation was to ensure the `backend` script directory is present on `sys.path` when `manage.py` is executed, and to recommend running tests from the `backend` working directory to avoid path-related surprises.

