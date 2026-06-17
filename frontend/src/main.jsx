import React, { Suspense, lazy, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import { clearAuthTokens, getAccessToken, getProfile, login, register } from "./services/api.js";

const QaPage = lazy(() => import("./pages/QaPage.jsx"));
const MorphologyPage = lazy(() => import("./pages/MorphologyPage.jsx"));
const CognatesPage = lazy(() => import("./pages/CognatesPage.jsx"));
const SearchPage = lazy(() => import("./pages/SearchPage.jsx"));
const HistoricalPage = lazy(() => import("./pages/HistoricalPage.jsx"));
const AnalyticsPage = lazy(() => import("./pages/AnalyticsPage.jsx"));
const NotFoundPage = lazy(() => import("./pages/NotFoundPage.jsx"));

export const LANGUAGES = [
  ["uz", "Uzbek"],
  ["tr", "Turkish"],
  ["az", "Azerbaijani"],
  ["kk", "Kazakh"],
  ["ky", "Kyrgyz"],
  ["tk", "Turkmen"],
  ["ug", "Uyghur"],
  ["otk", "Old Turkic"],
];

const ROUTES = [
  { path: "/qa", label: "QA Chat", description: "Evidence-backed answers", page: QaPage },
  { path: "/morphology", label: "Morphology", description: "Analyze word forms", page: MorphologyPage },
  { path: "/cognates", label: "Cognates", description: "Explore shared roots", page: CognatesPage },
  { path: "/search", label: "Semantic Search", description: "Find related forms", page: SearchPage },
  { path: "/historical", label: "Historical", description: "Trace evolution", page: HistoricalPage },
  { path: "/analytics", label: "Analytics", description: "Admin insights", page: AnalyticsPage, admin: true },
];

function currentPath() {
  const path = window.location.pathname === "/" ? "/qa" : window.location.pathname;
  return ROUTES.some((route) => route.path === path) ? path : window.location.pathname;
}

function navigate(path) {
  window.history.pushState({}, "", path);
  window.dispatchEvent(new PopStateEvent("popstate"));
}

function App() {
  const [path, setPath] = useState(currentPath());
  const [auth, setAuth] = useState({ token: getAccessToken(), profile: null, loading: Boolean(getAccessToken()) });
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const onPop = () => setPath(currentPath());
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);

  useEffect(() => {
    if (!auth.token) return;
    getProfile()
      .then((profile) => setAuth((state) => ({ ...state, profile, loading: false })))
      .catch(() => setAuth((state) => ({ ...state, profile: null, loading: false })));
  }, [auth.token]);

  useEffect(() => {
    if (!toast) return undefined;
    const timer = window.setTimeout(() => setToast(null), 3200);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const route = ROUTES.find((item) => item.path === path);
  const Page = route?.page || NotFoundPage;
  const authValue = useMemo(() => ({
    ...auth,
    isAdmin: auth.profile?.user?.role === "SUPER_ADMIN" || auth.profile?.user?.is_staff,
    async signIn(email, password) {
      const tokens = await login(email, password);
      setAuth({ token: tokens.access, profile: null, loading: true });
      setToast({ type: "success", message: "Signed in" });
    },
    async signUp(payload) {
      await register(payload);
      setToast({ type: "success", message: "Account created. Sign in to continue." });
    },
    signOut() {
      clearAuthTokens();
      setAuth({ token: "", profile: null, loading: false });
      setToast({ type: "success", message: "Signed out" });
      if (path === "/analytics") navigate("/qa");
    },
    notify(message, type = "success") {
      setToast({ type, message });
    },
  }), [auth, path]);

  return (
    <AuthContext.Provider value={authValue}>
      <div className="app-shell">
        <aside className="sidebar">
          <button className="brand-block" type="button" onClick={() => navigate("/qa")}>
            <div className="brand-mark">T</div>
            <div>
              <h1>TurkicGrammarAI</h1>
              <p>Scientific Turkic language tools</p>
            </div>
          </button>
          <nav className="nav-list" aria-label="Primary">
            {ROUTES.map((item) => (
              <button
                key={item.path}
                className={path === item.path ? "nav-item active" : "nav-item"}
                onClick={() => navigate(item.path)}
                type="button"
              >
                <span>{item.label}</span>
                <small>{item.description}</small>
              </button>
            ))}
          </nav>
          <SessionPanel />
        </aside>
        <main className="workspace">
          <ErrorBoundary>
            {route?.admin && !authValue.token ? (
              <AuthPage />
            ) : route?.admin && authValue.loading ? (
              <PageSkeleton />
            ) : route?.admin && !authValue.isAdmin ? (
              <ForbiddenPage />
            ) : (
              <Suspense fallback={<PageSkeleton />}>
                <Page />
              </Suspense>
            )}
          </ErrorBoundary>
        </main>
        {toast && <Toast toast={toast} onClose={() => setToast(null)} />}
      </div>
    </AuthContext.Provider>
  );
}

export const AuthContext = React.createContext(null);

function SessionPanel() {
  const auth = React.useContext(AuthContext);
  return (
    <div className="system-panel">
      <span className="status-dot" />
      {auth.token ? (
        <>
          <strong>{auth.profile?.user?.email || "Signed in"}</strong>
          <button className="link-button" type="button" onClick={auth.signOut}>Logout</button>
        </>
      ) : (
        <>
          <strong>Public session</strong>
          <button className="link-button" type="button" onClick={() => navigate("/analytics")}>Admin login</button>
        </>
      )}
    </div>
  );
}

function AuthPage() {
  const auth = React.useContext(AuthContext);
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ email: "", password: "", first_name: "", last_name: "", role: "RESEARCHER" });
  const [state, setState] = useState({ loading: false, error: "" });

  async function submit(event) {
    event.preventDefault();
    setState({ loading: true, error: "" });
    try {
      if (mode === "login") await auth.signIn(form.email, form.password);
      else await auth.signUp(form);
      setState({ loading: false, error: "" });
      if (mode === "register") setMode("login");
    } catch (error) {
      setState({ loading: false, error: error.message || "Authentication failed" });
    }
  }

  return (
    <section className="narrow-page">
      <PageHeader title="Admin Access" eyebrow="Protected analytics" />
      <form className="auth-card" onSubmit={submit}>
        <div className="segmented">
          <button type="button" className={mode === "login" ? "active" : ""} onClick={() => setMode("login")}>Login</button>
          <button type="button" className={mode === "register" ? "active" : ""} onClick={() => setMode("register")}>Register</button>
        </div>
        {mode === "register" && (
          <div className="form-grid two">
            <input value={form.first_name} onChange={(event) => setForm({ ...form, first_name: event.target.value })} placeholder="First name" />
            <input value={form.last_name} onChange={(event) => setForm({ ...form, last_name: event.target.value })} placeholder="Last name" />
          </div>
        )}
        <input value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} placeholder="Email" type="email" required />
        <input value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} placeholder="Password" type="password" required />
        {state.error && <div className="status error">{state.error}</div>}
        <button className="primary-button" type="submit" disabled={state.loading}>{state.loading ? "Working" : mode === "login" ? "Login" : "Register"}</button>
      </form>
    </section>
  );
}

function ForbiddenPage() {
  const auth = React.useContext(AuthContext);
  return (
    <section className="narrow-page">
      <PageHeader title="Admin Role Required" eyebrow="403" />
      <div className="panel">
        <p>This dashboard is restricted to Super Admin accounts.</p>
        <button className="secondary-button" type="button" onClick={auth.signOut}>Use another account</button>
      </div>
    </section>
  );
}

export function PageHeader({ title, eyebrow, actions }) {
  return (
    <header className="page-header">
      <div>
        <p>{eyebrow}</p>
        <h2>{title}</h2>
      </div>
      {actions}
    </header>
  );
}

export function PageSkeleton() {
  return (
    <div className="skeleton-stack">
      <div className="skeleton title" />
      <div className="skeleton input" />
      <div className="skeleton panel" />
      <div className="skeleton panel small" />
    </div>
  );
}

function Toast({ toast, onClose }) {
  return (
    <div className={`toast ${toast.type}`}>
      <span>{toast.message}</span>
      <button type="button" onClick={onClose}>Close</button>
    </div>
  );
}

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { failed: false };
  }

  static getDerivedStateFromError() {
    return { failed: true };
  }

  render() {
    if (this.state.failed) {
      return (
        <section className="narrow-page">
          <PageHeader title="Application Error" eyebrow="500" />
          <div className="panel">
            <p>The interface hit an unexpected rendering error.</p>
            <button className="primary-button" type="button" onClick={() => window.location.reload()}>Reload</button>
          </div>
        </section>
      );
    }
    return this.props.children;
  }
}

createRoot(document.getElementById("root")).render(<App />);
