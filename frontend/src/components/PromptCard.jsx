import "./PromptCard.css";

export default function PromptCard({ children, onClick, disabled }) {
  return (
    <button
      type="button"
      className="prompt-card"
      onClick={onClick}
      disabled={disabled}
    >
      <span className="prompt-card__icon" aria-hidden>
        ✦
      </span>
      <span className="prompt-card__text">{children}</span>
    </button>
  );
}
