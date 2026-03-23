import { Card, IconBadge } from "../ui/index.js";
import "./DocMiniCard.css";

export default function DocMiniCard({ icon, title, description }) {
  return (
    <Card variant="nested" className="doc-mini-card">
      <IconBadge size="md" aria-hidden>
        {icon}
      </IconBadge>
      <h3 className="doc-mini-card__title">{title}</h3>
      <p className="doc-mini-card__desc">{description}</p>
    </Card>
  );
}
