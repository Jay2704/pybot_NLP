import { Pill } from "./ui/index.js";
import "./TopicsCard.css";

const DEFAULT_TOPICS = ["Pandas Merge", "Asyncio Loops", "Django Auth"];

export default function TopicsCard({ topics = DEFAULT_TOPICS }) {
  return (
    <section className="topics-card" aria-label="Recent topics">
      <h3 className="topics-card__title">Recent Topics</h3>
      <ul className="topics-card__pills">
        {topics.map((t) => (
          <li key={t}>
            <Pill as="span" variant="topic-label">
              {t}
            </Pill>
          </li>
        ))}
      </ul>
    </section>
  );
}
