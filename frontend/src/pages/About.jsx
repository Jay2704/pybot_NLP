import { Button } from "../components/ui/index.js";
import ProfileAvatar from "../components/ProfileAvatar.jsx";
import { PORTFOLIO_URL, GITHUB_REPO_URL } from "../constants/branding.js";
import "./About.css";

export default function About() {
  return (
    <section className="about-page">
      <div className="about-page__inner">
        <header className="about-page__header">
          <h1 className="about-page__title">About the Developer</h1>
          <p className="about-page__subtitle">
            Meet the engineer behind PyBot AI — built for clarity, speed, and a premium chat
            experience.
          </p>
        </header>

        <article className="about-developer">
          <div className="about-developer__media">
            <ProfileAvatar size="lg" alt="Jay — Software Engineer and AI Developer" />
          </div>
          <div className="about-developer__body">
            <h2 className="about-developer__name">Jay</h2>
            <p className="about-developer__title">Software Engineer / AI Developer</p>
            <div className="about-developer__bio">
              <p>
                I design and ship AI systems that feel fast, reliable, and easy to use—from
                retrieval and ranking to polished product surfaces. My work spans full-stack
                development, with a focus on scalable architecture and interfaces that stay calm
                under real traffic.
              </p>
              <p>
                PyBot AI is an example of that approach: a production-style chatbot experience
                pairing a modern React frontend with a FastAPI backend, tuned for helpful answers
                and a SaaS-quality user experience.
              </p>
            </div>
            <div className="about-developer__actions">
              <Button
                as="a"
                href={PORTFOLIO_URL}
                target="_blank"
                rel="noopener noreferrer"
                variant="primary"
                size="md"
              >
                View Portfolio
              </Button>
              <Button
                as="a"
                href={GITHUB_REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                variant="outline"
                size="md"
              >
                GitHub
              </Button>
            </div>
          </div>
        </article>
      </div>
    </section>
  );
}
