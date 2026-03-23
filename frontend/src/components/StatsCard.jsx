import "./StatsCard.css";

export default function StatsCard({ totalQueries, avgResponseLabel }) {
  return (
    <section className="stats-card" aria-label="Session statistics">
      <h3 className="stats-card__title">Session stats</h3>
      <div className="stats-card__grid">
        <div className="stats-card__item">
          <span className="stats-card__icon" aria-hidden>
            📊
          </span>
          <div>
            <div className="stats-card__value">{totalQueries}</div>
            <div className="stats-card__label">Total Queries</div>
          </div>
        </div>
        <div className="stats-card__item">
          <span className="stats-card__icon" aria-hidden>
            ⚡
          </span>
          <div>
            <div className="stats-card__value">{avgResponseLabel}</div>
            <div className="stats-card__label">Avg. Response</div>
          </div>
        </div>
      </div>
    </section>
  );
}
