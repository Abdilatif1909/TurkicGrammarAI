import React from "react";
import { LANGUAGES, PageHeader } from "../main.jsx";
import { apiGet } from "../services/api.js";
import { EmptyState, QueryForm, RadialGraph, ResultTable, Status, formatNumber, useAsyncAction } from "./shared.jsx";

export default function CognatesPage() {
  const [query, setQuery] = React.useState("tangri");
  const [language, setLanguage] = React.useState("");
  const [state, search] = useAsyncAction((q, lang) => apiGet("/api/cognates/universal-search/", { q, language: lang, limit: 20 }));
  const results = state.data?.results || [];
  const selected = results[0];

  function submit(event) {
    event.preventDefault();
    search(query, language);
  }

  return (
    <section>
      <PageHeader title="Cognate Explorer" eyebrow="Cross-language cognate groups and history" />
      <QueryForm value={query} setValue={setQuery} onSubmit={submit} loading={state.loading} placeholder="Search a form or proto-form">
        <select value={language} onChange={(event) => setLanguage(event.target.value)}>
          <option value="">All languages</option>
          {LANGUAGES.map(([code, label]) => <option value={code} key={code}>{label}</option>)}
        </select>
      </QueryForm>
      <Status state={state} />
      <div className="two-column">
        <div className="panel">
          <h3>Cognate Table</h3>
          <ResultTable rows={results} columns={[
            { key: "cognate_id", label: "Group" },
            { key: "proto_form", label: "Proto" },
            { key: "semantic_domain", label: "Domain" },
            { key: "confidence", label: "Confidence", render: (row) => formatNumber(row.confidence) },
          ]} />
        </div>
        <div className="panel">
          <h3>Graph and Chain</h3>
          {selected ? (
            <>
              <RadialGraph nodes={[selected.proto_form, ...Object.entries(selected.forms || {}).map(([lang, form]) => `${lang}: ${form}`)]} />
              <div className="timeline">
                {(selected.historical_chain || selected.historical_lineage || []).map((item, index) => (
                  <div className="timeline-item" key={`${item.stage || index}-${item.form || index}`}>
                    <strong>{item.stage || `Step ${index + 1}`}</strong>
                    <span>{item.form || item}</span>
                  </div>
                ))}
              </div>
            </>
          ) : <EmptyState>No cognate selected.</EmptyState>}
        </div>
      </div>
    </section>
  );
}
