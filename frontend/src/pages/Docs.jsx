import DocCard from "../components/docs/DocCard.jsx";
import DocMiniCard from "../components/docs/DocMiniCard.jsx";
import DocCompactCard from "../components/docs/DocCompactCard.jsx";
import "./Docs.css";

export default function Docs() {
  return (
    <div className="docs-page">
      <div className="docs-page__inner">
        <header className="docs-page__header">
          <h1 className="docs-page__title">Documentation</h1>
          <p className="docs-page__subtitle">
            PyBot AI is a portfolio-grade Python Q&amp;A experience: a retrieval-backed assistant
            with a modern web UI, REST API, and one-click deployment story—documented here at a
            glance.
          </p>
        </header>

        <div className="docs-page__grid-2">
          <DocCard title="Overview" eyebrow="Product">
            <p>
              This chatbot is a <strong>retrieval-based</strong> Python Q&amp;A assistant. It does
              not hallucinate from scratch: it finds the closest matching questions in a{" "}
              <strong>Stack Overflow–derived knowledge base</strong>, then returns the best-scoring
              answer for your prompt—ideal for demos that emphasize classic NLP and transparent
              sourcing.
            </p>
            <div className="docs-page__minis">
              <DocMiniCard
                icon="🎯"
                title="Targeted Intent"
                description="Optimized for Python programming questions—syntax, idioms, libraries, and common pitfalls."
              />
              <DocMiniCard
                icon="🧠"
                title="Context Aware"
                description="Uses retrieved Q&amp;A context from curated pairs so replies align with real Stack Overflow discussions."
              />
            </div>
          </DocCard>

          <DocCard title="Architecture" eyebrow="System">
            <ul className="docs-page__arch-list">
              <li>
                <strong>React</strong> frontend (Vite) with a chat UI and marketing pages
              </li>
              <li>
                <strong>FastAPI</strong> backend serving JSON for the chat client
              </li>
              <li>
                <strong>TF-IDF</strong> vectorization and <strong>cosine similarity</strong> for
                retrieval over question embeddings
              </li>
              <li>
                <strong>Stack Overflow</strong> processed knowledge base (question–answer pairs)
              </li>
              <li>
                <strong>Docker</strong> image deployable to <strong>Hugging Face Spaces</strong>{" "}
                (single container for API + static UI)
              </li>
            </ul>
          </DocCard>
        </div>

        <p className="docs-page__section-label">Reference</p>
        <div className="docs-page__compact-grid">
          <DocCompactCard icon="🔌" title="Client &amp; server">
            <p>
              The React app talks to the FastAPI service using the shared client in{" "}
              <code>frontend/src/services/api.js</code>. Production builds typically use{" "}
              <strong>same-origin</strong> requests; local development can use the Vite dev
              proxy or a configured API base URL—see project deployment notes in the repo.
            </p>
            <p>
              Response fields surfaced in the UI include answer text and retrieval metadata for
              transparency (exact field names are defined by the running API and parsed in{" "}
              <code>api.js</code>).
            </p>
          </DocCompactCard>

          <DocCompactCard icon="🔍" title="Retrieval Flow">
            <p>User message → text cleanup → TF-IDF query vector → cosine similarity vs. index →</p>
            <ul>
              <li>Pick nearest question row</li>
              <li>Resolve best answer among duplicates by score / date rules</li>
              <li>Return answer payload to the UI</li>
            </ul>
          </DocCompactCard>

          <DocCompactCard icon="🚀" title="Deployment Notes">
            <p>
              Build the React app into static files; run FastAPI with Uvicorn. The Docker image
              bundles both. On Hugging Face, ensure retrieval <code>.pkl</code> artifacts and data
              ship in the image or volume per your ops checklist.
            </p>
          </DocCompactCard>
        </div>
      </div>
    </div>
  );
}
