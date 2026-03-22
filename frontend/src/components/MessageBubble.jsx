import "./MessageBubble.css";

export default function MessageBubble({ role, text, meta }) {
  const isUser = role === "user";

  return (
    <div className={`message-row ${isUser ? "message-row--user" : "message-row--bot"}`}>
      <div className={`message-bubble ${isUser ? "message-bubble--user" : "message-bubble--bot"}`}>
        <div className="message-bubble__label">{isUser ? "You" : "PyBot"}</div>
        <div className="message-bubble__text">{text}</div>
        {!isUser && meta && (
          <div className="message-bubble__meta">
            QId {meta.qid} · AId {meta.aid}
            {meta.alternate != null && ` · score ${meta.alternate}`}
          </div>
        )}
      </div>
    </div>
  );
}
