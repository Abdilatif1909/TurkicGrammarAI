import React from "react";
import { PageHeader } from "../main.jsx";
import { apiGet } from "../services/api.js";
import { EmptyState, LinearGraph, QueryForm, ResultTable, Status, useAsyncAction } from "./shared.jsx";

export default function HistoricalPage() {
  const [query, setQuery] = React.useState("tangri");
  const [state, retrieve] = useAsyncAction((q) => apiGet("/api/rag/retrieve/", { q, topn: 12 }));
  const docs = state.data?.retrieved_documents || [];
  const selected = docs.find((item) => item.historical_lineage?.length) || docs[0];
  const lineage = selected?.historical_lineage || [];

  function submit(event) {
    event.preventDefault();
    retrieve(query);
  }

  return (
    <section>
      <PageHeader title="Historical Evolution Explorer" eyebrow="Lineage graph, timeline, and source details" />
      <QueryForm value={query} setValue={setQuery} onSubmit={submit} loading={state.loading} placeholder="Enter a historical or modern form" />
      <Status state={state} />
      <div className="two-column">
        <div className="panel">
          <h3>Lineage Graph</h3>
          <LinearGraph nodes={lineage.map((item) => `${item.stage}: ${item.form}`)} accent="blue" />
          <h3>Timeline</h3>
          <div className="timeline">
            {lineage.length ? lineage.map((item, index) => (
              <button className="timeline-item" type="button" key={`${item.stage}-${index}`}>
                <strong>{item.stage}</strong>
                <span>{item.form}</span>
              </button>
            )) : <EmptyState>No lineage returned.</EmptyState>}
          </div>
        </div>
        <div className="panel">
          <h3>Node Details</h3>
          {selected ? <pre className="metric-json">{JSON.stringify(selected, null, 2)}</pre> : <EmptyState>No selected node.</EmptyState>}
          <ResultTable rows={docs} columns={[
            { key: "word", label: "Word" },
            { key: "language", label: "Language" },
            { key: "source_type", label: "Source" },
            { key: "source_id", label: "Source ID" },
          ]} />
        </div>
      </div>
    </section>
  );
}
