import FeatureCard from "../components/FeatureCard.jsx";
import TechPill from "../components/TechPill.jsx";
import { SectionHeader } from "../components/ui/index.js";
import "./Features.css";

const FEATURES = [
  {
    icon: "🐍",
    title: "Python Q&A",
    description:
      "Ask natural-language Python questions and receive answers grounded in retrieval over curated programming knowledge.",
  },
  {
    icon: "⚡",
    title: "FastAPI Backend",
    description:
      "A high-performance async API with automatic OpenAPI docs, health checks, and a clean JSON contract for the chat UI.",
  },
  {
    icon: "⚛️",
    title: "React Frontend",
    description:
      "A responsive single-page app with a polished chat experience, sample prompts, and same-origin deployment support.",
  },
  {
    icon: "📚",
    title: "Stack Overflow DB",
    description:
      "Train and serve on real-world Q&A pairs sourced from Stack Overflow–style data for relevant, practical answers.",
  },
  {
    icon: "◎",
    title: "TF-IDF Matching",
    description:
      "Classic TF-IDF vectorization and cosine similarity for fast, interpretable nearest-question retrieval.",
  },
  {
    icon: "🤗",
    title: "Hugging Face Deployment",
    description:
      "Ship as a single Docker Space: one container runs the API and the built React app for simple demos and portfolios.",
  },
];

const STACK = [
  { label: "Frontend", pills: ["React", "Vite"] },
  { label: "Backend", pills: ["FastAPI", "Pydantic"] },
  { label: "ML & AI", pills: ["Hugging Face", "TF-IDF"] },
  { label: "Data", pills: ["Stack Overflow dataset", "processed Q&A"] },
  { label: "DevOps", pills: ["Docker", "Hugging Face Spaces"] },
];

export default function Features() {
  return (
    <div className="features-page">
      <div className="features-page__inner">
        <SectionHeader
          size="hero"
          align="center"
          titleAs="h1"
          title={
            <>
              Built for <span className="ui-section-header__highlight">modern</span> Python Q&amp;A
            </>
          }
          subtitle="Everything you need to demo retrieval-powered answers—from vectorized search to a production-style API and deployable frontend—in one cohesive stack."
        />

        <section className="features-grid" aria-label="Product features">
          {FEATURES.map((f) => (
            <FeatureCard key={f.title} icon={f.icon} title={f.title} description={f.description} />
          ))}
        </section>

        <section className="features-stack" aria-labelledby="arch-stack-heading">
          <h2 id="arch-stack-heading" className="features-stack__title">
            Architectural Stack
          </h2>
          <div className="features-stack__groups">
            {STACK.map((group) => (
              <div key={group.label} className="features-stack__row">
                <p className="features-stack__label">{group.label}</p>
                <div className="features-stack__pills">
                  {group.pills.map((p) => (
                    <TechPill key={p}>{p}</TechPill>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
