import React from "react";
import { PageHeader } from "../main.jsx";
import { apiGet } from "../services/api.js";
import { EmptyState, QueryForm, ResultTable, Status, formatNumber, useAsyncAction } from "./shared.jsx";

const PAGE_SIZE = 10;

export default function SearchPage() {
  const [query, setQuery] = React.useState("tangri");
  const [page, setPage] = React.useState(1);
  const [state, search] = useAsyncAction((q) => apiGet("/api/search/semantic/", { q, topn: 50 }));
  const results = state.data?.results || [];
  const pageRows = results.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
  const totalPages = Math.max(1, Math.ceil(results.length / PAGE_SIZE));

  function submit(event) {
    event.preventDefault();
    setPage(1);
    search(query);
  }

  return (
    <section>
      <PageHeader title="Semantic Search" eyebrow="Exact, morphology, cognate, historical, cross-language retrieval" />
      <QueryForm value={query} setValue={setQuery} onSubmit={submit} loading={state.loading} placeholder="Search semantic neighbors" />
      <Status state={state} />
      {!results.length && !state.loading ? <EmptyState>No search results yet.</EmptyState> : (
        <>
          <ResultTable rows={pageRows} columns={[
            { key: "word", label: "Word" },
            { key: "language", label: "Language", render: (row) => <span className="badge">{row.language}</span> },
            { key: "cognate_group", label: "Cognate" },
            { key: "similarity", label: "Similarity", render: (row) => formatNumber(row.similarity) },
            { key: "score", label: "Score", render: (row) => formatNumber(row.score) },
            { key: "search_types", label: "Type", render: (row) => (row.search_types || []).join(", ") },
          ]} />
          <div className="pagination">
            <button type="button" disabled={page <= 1} onClick={() => setPage((value) => value - 1)}>Previous</button>
            <span>Page {page} of {totalPages}</span>
            <button type="button" disabled={page >= totalPages} onClick={() => setPage((value) => value + 1)}>Next</button>
          </div>
        </>
      )}
    </section>
  );
}
