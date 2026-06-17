import React from "react";
import { AuthContext, PageHeader } from "../main.jsx";
import { apiGet, postJson } from "../services/api.js";
import { EmptyState, ResultTable, Status, QueryForm, formatNumber, useAsyncAction } from "./shared.jsx";

export default function QaPage() {
  const auth = React.useContext(AuthContext);
  const [question, setQuestion] = React.useState("Tangri sozining turkiy tillardagi shakllari qanday?");
  const [history, setHistory] = React.useState(() => JSON.parse(window.localStorage.getItem("turkicgrammarai.qaHistory") || "[]"));
  const [state, ask] = useAsyncAction((q) => apiGet("/api/qa/ask/", { q, topk: 8 }));

  React.useEffect(() => {
    window.localStorage.setItem("turkicgrammarai.qaHistory", JSON.stringify(history.slice(0, 12)));
  }, [history]);

  async function submit(event) {
    event.preventDefault();
    const data = await ask(question);
    if (data) setHistory((items) => [{ question, data, createdAt: new Date().toISOString() }, ...items].slice(0, 12));
  }

  function copyAnswer(answer) {
    navigator.clipboard?.writeText(answer);
    auth.notify("Answer copied");
  }

  return (
    <section>
      <PageHeader
        title="QA Chat"
        eyebrow="Retrieval-based answers with citations"
        actions={<button className="secondary-button" type="button" onClick={() => setHistory([])}>Clear chat</button>}
      />
      <QueryForm value={question} setValue={setQuestion} onSubmit={submit} loading={state.loading} placeholder="Ask a Turkic linguistics question" button="Ask" />
      <Status state={state} />
      <div className="chat-stack">
        {!history.length && !state.loading && <EmptyState>Ask a question to build a cited answer history.</EmptyState>}
        {history.map((item, index) => (
          <article className="answer-block" key={`${item.question}-${index}`}>
            <div className="question-line">{item.question}</div>
            <p className="answer-text">{item.data.answer}</p>
            <div className="toolbar-row">
              <button className="secondary-button" type="button" onClick={() => copyAnswer(item.data.answer)}>Copy answer</button>
              <span className="muted">{item.data.question_type} · query: {item.data.query_term}</span>
            </div>
            <CitationStrip citations={item.data.citations} />
            <FeedbackForm question={item.question} answer={item.data.answer} retrievedSources={item.data.support_documents} />
            <ResultTable rows={item.data.items || []} columns={[
              { key: "word", label: "Word", render: (row) => row.word || row.lemma },
              { key: "language_name", label: "Language" },
              { key: "cognate_group", label: "Cognate" },
              { key: "confidence", label: "Confidence", render: (row) => formatNumber(row.confidence) },
              { key: "source_type", label: "Source" },
            ]} />
          </article>
        ))}
      </div>
    </section>
  );
}

function CitationStrip({ citations }) {
  if (!citations?.length) return <EmptyState>No citations returned.</EmptyState>;
  return (
    <div className="citation-strip">
      {citations.map((citation, index) => (
        <span key={`${citation.source_type}-${citation.source_id}-${index}`}>
          {citation.source_type}:{citation.source_id || "n/a"} · {formatNumber(citation.confidence)}
        </span>
      ))}
    </div>
  );
}

function FeedbackForm({ question, answer, retrievedSources }) {
  const auth = React.useContext(AuthContext);
  const [rating, setRating] = React.useState("5");
  const [comment, setComment] = React.useState("");
  const [state, send] = useAsyncAction((payload) => postJson("/api/feedback/", payload));

  async function submit(event) {
    event.preventDefault();
    const result = await send({ question, answer, rating: Number(rating), comment, retrieved_sources: retrievedSources || [] });
    if (result) {
      setComment("");
      auth.notify("Feedback saved");
    }
  }

  return (
    <form className="feedback-form" onSubmit={submit}>
      <select value={rating} onChange={(event) => setRating(event.target.value)} aria-label="Rating">
        <option value="5">5 useful</option>
        <option value="4">4 good</option>
        <option value="3">3 mixed</option>
        <option value="2">2 weak</option>
        <option value="1">1 wrong</option>
      </select>
      <input value={comment} onChange={(event) => setComment(event.target.value)} placeholder="Feedback comment" />
      <button type="submit" disabled={state.loading}>{state.loading ? "Sending" : "Send feedback"}</button>
      {state.error && <span className="inline-error">{state.error}</span>}
    </form>
  );
}
