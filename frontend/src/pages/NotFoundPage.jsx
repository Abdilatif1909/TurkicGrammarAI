import React from "react";
import { PageHeader } from "../main.jsx";

export default function NotFoundPage() {
  return (
    <section className="narrow-page">
      <PageHeader title="Page Not Found" eyebrow="404" />
      <div className="panel">
        <p>The requested page does not exist in TurkicGrammarAI.</p>
        <a className="secondary-link" href="/qa">Go to QA Chat</a>
      </div>
    </section>
  );
}
