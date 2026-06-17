# Frontend Production Audit

Audit date: 2026-06-17

Scope: `frontend/src`, `frontend/package.json`, `frontend/vite.config.js`, `frontend/dist`, and backend API integration.

Build check: `npm run build` passed on 2026-06-17.

## Summary

The React frontend is small and functional, but it is closer to a demo dashboard than a production research UI. It uses custom routing, plain fetch helpers, JWT localStorage, no frontend tests, and minimal accessibility/mobile verification. The build succeeds, but production readiness is limited by test gaps, security tradeoffs, and error-handling depth.

## Findings

### 1. No frontend test stack

- File: `frontend/package.json`
- Risk: high
- Evidence: scripts only include `dev`, `build`, and `preview`.
- Recommendation: add component tests for shared controls and API client; add Playwright smoke tests for QA/Morphology/Admin login.

### 2. JWT tokens are stored in localStorage

- File: `frontend/src/services/api.js`
- Risk: medium-high
- Evidence: access/refresh tokens use `window.localStorage`.
- Recommendation: for production, prefer HttpOnly secure refresh cookie or strict CSP plus short refresh rotation.

### 3. Custom routing lacks mature guards

- File: `frontend/src/main.jsx`
- Risk: medium
- Evidence: routing is manual `window.history.pushState`; protected route logic only guards Analytics admin view.
- Recommendation: add route tests or use React Router.

### 4. API error messages surface raw response text

- File: `frontend/src/services/api.js`
- Risk: medium
- Evidence: failed requests throw `new Error(text || ...)`.
- Recommendation: parse JSON error envelopes and show normalized messages.

### 5. Loading states exist but cancelation/race handling does not

- Files: `frontend/src/pages/*.jsx`, `frontend/src/pages/shared.jsx`
- Risk: medium
- Recommendation: add AbortController or stale-response guard for repeated searches.

### 6. Admin registration is exposed from admin login UI

- File: `frontend/src/main.jsx`
- Endpoint: `/api/auth/register/`
- Risk: medium
- Evidence: protected Analytics view offers Register mode with `role: "RESEARCHER"` in form state.
- Recommendation: separate public registration from admin access.

### 7. Mobile UX is unverified

- File: `frontend/src/styles.css`
- Risk: medium
- Evidence: fixed 300px sidebar grid is the default app shell.
- Recommendation: add Playwright screenshots for 375px, 768px, and desktop widths.

### 8. Frontend uses current `/api/` contract

- Files: `frontend/src/services/api.js`, pages under `frontend/src/pages`
- Risk: low for current app, high if docs stay `/api/v1/`.
- Recommendation: keep aligned with backend and fix docs, or introduce one API version config.

### 9. No lint/typecheck enforcement

- File: `frontend/package.json`
- Risk: medium
- Evidence: no `lint`, no `typecheck`, no TypeScript source despite TypeScript dependency.
- Recommendation: add ESLint and typecheck or remove unused TypeScript dependency.

### 10. Production build assets are committed

- Files: `frontend/dist/*`
- Risk: low-medium
- Recommendation: decide whether `dist` is deployment artifact or generated output. If generated, exclude from source control and build in CI.

## Production Actions

1. Add frontend test tooling and smoke E2E.
2. Normalize API errors.
3. Add responsive/mobile screenshots.
4. Revisit token storage.
5. Align docs and frontend API prefix.

