import { Link } from "react-router-dom";
import { Button, Pill } from "../components/ui/index.js";
import "./Home.css";

function ChatPreviewMockup() {
  return (
    <div className="home__preview-card" aria-hidden="true">
      <div className="home__mock-header">
        <div className="home__mock-dots" aria-hidden>
          <span />
          <span />
          <span />
        </div>
        <span className="home__mock-title">PyBot AI</span>
        <span style={{ width: 40 }} aria-hidden />
      </div>

      <div className="home__mock-msg home__mock-msg--user">
        <div className="home__mock-bubble home__mock-bubble--user">
          What is list comprehension in Python?
        </div>
      </div>

      <div className="home__mock-msg">
        <div className="home__mock-bubble home__mock-bubble--bot">
          Here’s a compact way to build lists—nested loops are allowed in one expression:
          <pre className="home__mock-code">
            <code>{`[y for x in range(3) for y in [x, x]]`}</code>
          </pre>
          <span className="home__mock-source">Source: Stack Overflow</span>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <section className="home">
      <div className="home__hero">
        <div className="home__copy">
          <Pill variant="badge">93k+ Stack Overflow pairs processed</Pill>
          <h1 className="home__title">
            Ask <span className="home__highlight">Python</span> Questions Instantly
          </h1>
          <p className="home__sub">
            Get Python answers quickly using our AI-powered retrieval system trained on Stack
            Overflow knowledge.
          </p>
          <div className="home__ctas">
            <Button as={Link} to="/chat" variant="primary" size="md">
              Try the Chatbot
            </Button>
            <Button as={Link} to="/docs" variant="secondary" size="md">
              View Documentation
            </Button>
          </div>
        </div>

        <div className="home__preview">
          <ChatPreviewMockup />
        </div>
      </div>
    </section>
  );
}
