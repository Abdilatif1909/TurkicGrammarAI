import React from "react";
import { LANGUAGES, PageHeader } from "../main.jsx";
import { apiGet } from "../services/api.js";
import { EmptyState, LinearGraph, QueryForm, Status, formatNumber, normalizeSuffixes, useAsyncAction } from "./shared.jsx";

export default function MorphologyPage() {
  const [word, setWord] = React.useState("kitoblarimizdan");
  const [language, setLanguage] = React.useState("uz");
  const [showJson, setShowJson] = React.useState(false);
  const [state, analyze] = useAsyncAction((q, lang) => apiGet("/api/morphology/analyze/", { word: q, language: lang }));
  const analyses = state.data?.analyses || [];

  function submit(event) {
    event.preventDefault();
    analyze(word, language);
  }

  return (
    <section>
      <PageHeader
        title="Morphology Analyzer"
        eyebrow="Ranked roots, lemmas, suffix chains"
        actions={<button className="secondary-button" type="button" onClick={() => setShowJson((value) => !value)}>{showJson ? "Hide JSON" : "JSON view"}</button>}
      />
      <QueryForm value={word} setValue={setWord} onSubmit={submit} loading={state.loading} placeholder="Enter a word">
        <select value={language} onChange={(event) => setLanguage(event.target.value)}>
          {LANGUAGES.map(([code, label]) => <option value={code} key={code}>{label}</option>)}
        </select>
      </QueryForm>
      <Status state={state} />
      <div className="two-column">
        <div className="panel">
          <h3>Analyses</h3>
          {!analyses.length && !state.loading && <EmptyState>No analyses yet.</EmptyState>}
          {analyses.map((analysis, index) => <AnalysisCard analysis={analysis} rank={index + 1} key={index} />)}
        </div>
        <div className="panel">
          <h3>Morphology Tree</h3>
          <LinearGraph nodes={[analyses[0]?.root || word, ...normalizeSuffixes(analyses[0])]} accent="green" />
          {showJson && <pre className="metric-json">{JSON.stringify(state.data || {}, null, 2)}</pre>}
        </div>
      </div>
    </section>
  );
}

function AnalysisCard({ analysis, rank }) {
  const suffixes = normalizeSuffixes(analysis);
  return (
    <article className="analysis-card">
      <div className="card-title-row">
        <strong>#{rank} {analysis.lemma || analysis.word || analysis.surface}</strong>
        <span>{analysis.type || "morphology"}</span>
      </div>
      <span>root: {analysis.root || "n/a"}</span>
      <div className="chip-row">
        {suffixes.length ? suffixes.map((suffix, index) => <span className="chip" key={`${suffix}-${index}`}>{suffix}</span>) : <span className="chip muted-chip">no suffix</span>}
      </div>
      <small>score {formatNumber(analysis.score)} · confidence {formatNumber(analysis.confidence)}</small>
    </article>
  );
}
