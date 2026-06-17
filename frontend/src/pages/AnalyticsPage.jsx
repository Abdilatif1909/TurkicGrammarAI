import React from "react";
import { AuthContext, PageHeader } from "../main.jsx";
import { apiGet } from "../services/api.js";
import { EmptyState, ResultTable, Status, useAsyncAction } from "./shared.jsx";

export default function AnalyticsPage() {
  const auth = React.useContext(AuthContext);
  const [state, load] = useAsyncAction(async () => {
    const [usage, trends, words, languages, feedback, health] = await Promise.all([
      apiGet("/api/admin/analytics/usage/", { days: 30 }),
      apiGet("/api/admin/analytics/qa-trends/", { days: 30 }),
      apiGet("/api/admin/analytics/most-requested-words/", { limit: 20 }),
      apiGet("/api/admin/analytics/most-requested-languages/"),
      apiGet("/api/admin/feedback/"),
      apiGet("/api/analytics/health/"),
    ]);
    return { usage, trends, words, languages, feedback, health };
  });

  React.useEffect(() => {
    if (auth.token && auth.isAdmin) load();
  }, [auth.token, auth.isAdmin]);

  return (
    <section>
      <PageHeader title="Analytics Dashboard" eyebrow="Admin-only usage, quality, and feedback" actions={<button className="secondary-button" type="button" onClick={() => load()}>Refresh</button>} />
      <Status state={state} />
      {!state.data && !state.loading && <EmptyState>Sign in as an admin to load analytics.</EmptyState>}
      {state.data && (
        <>
          <div className="dashboard-grid">
            <MetricPanel title="Usage" data={state.data.usage} />
            <MetricPanel title="QA Trends" data={state.data.trends} />
            <MetricPanel title="Health" data={state.data.health} />
          </div>
          <div className="two-column">
            <div className="panel">
              <h3>Top Words</h3>
              <ResultTable rows={state.data.words.results || []} columns={[{ key: "query", label: "Word" }, { key: "count", label: "Count" }]} />
              <h3>Top Languages</h3>
              <ResultTable rows={state.data.languages.results || []} columns={[{ key: "language", label: "Language" }, { key: "count", label: "Count" }]} />
            </div>
            <div className="panel">
              <h3>Feedback</h3>
              <ResultTable rows={state.data.feedback.results || state.data.feedback || []} columns={[
                { key: "question", label: "Question" },
                { key: "rating", label: "Rating" },
                { key: "comment", label: "Comment" },
                { key: "created_at", label: "Created" },
              ]} />
            </div>
          </div>
        </>
      )}
    </section>
  );
}

function MetricPanel({ title, data }) {
  return (
    <div className="panel">
      <h3>{title}</h3>
      <pre className="metric-json">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
