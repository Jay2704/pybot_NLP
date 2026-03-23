import { Card, SectionHeader } from "../ui/index.js";
import "./DocCard.css";

export default function DocCard({ title, eyebrow, children }) {
  return (
    <Card variant="doc" as="article">
      <SectionHeader size="sm" align="left" eyebrow={eyebrow} title={title} />
      <div className="doc-card__body">{children}</div>
    </Card>
  );
}
