import { Card, IconBadge } from "./ui/index.js";
import "./FeatureCard.css";

export default function FeatureCard({ icon, title, description }) {
  return (
    <Card variant="feature" as="article">
      <IconBadge size="lg" aria-hidden>
        {icon}
      </IconBadge>
      <h3 className="feature-card__title">{title}</h3>
      <p className="feature-card__description">{description}</p>
    </Card>
  );
}
