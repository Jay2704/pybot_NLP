import "./MessageBubble.css";

function formatMessageTime(at) {
  if (at == null) return null;
  try {
    return new Date(at).toLocaleTimeString(undefined, {
      hour: "numeric",
      minute: "2-digit",
    });
  } catch {
    return null;
  }
}

export default function MessageBubble({ role, text, meta, at, variant = "default" }) {
  const isUser = role === "user";
  const timeLabel = formatMessageTime(at);
  const dash = variant === "dashboard";

  return (
    <div className={`message-row ${isUser ? "message-row--user" : "message-row--bot"}`}>
      <div
        className={`message-bubble ${isUser ? "message-bubble--user" : "message-bubble--bot"} ${
          dash ? "message-bubble--dashboard" : ""
        }`}
      >
        <div className="message-bubble__header">
          <span className="message-bubble__label">{isUser ? "You" : "PyBot"}</span>
          {timeLabel && (
            <time className="message-bubble__time" dateTime={typeof at === "number" ? new Date(at).toISOString() : undefined}>
              {timeLabel}
            </time>
          )}
        </div>
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
