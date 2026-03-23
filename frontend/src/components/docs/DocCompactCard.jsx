import "./DocCompactCard.css";

export default function DocCompactCard({ icon, title, children }) {
  return (
    <article className="doc-compact-card">
      <div className="doc-compact-card__head">
        <div className="doc-compact-card__icon" aria-hidden>
          {icon}
        </div>
        <h3 className="doc-compact-card__title">{title}</h3>
      </div>
      <div className="doc-compact-card__body">{children}</div>
    </article>
  );
}
