import "./ChatInputBar.css";

export default function ChatInputBar({
  value,
  onChange,
  onSubmit,
  loading,
  disabled,
}) {
  return (
    <form className="chat-input-bar" onSubmit={onSubmit}>
      <input
        type="text"
        className="chat-input-bar__field"
        placeholder="Ask anything about Python…"
        value={value}
        onChange={onChange}
        disabled={disabled}
        autoComplete="off"
        aria-label="Message"
      />
      <button
        type="submit"
        className="chat-input-bar__send"
        disabled={disabled || loading || !value.trim()}
        aria-label="Send message"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden>
          <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
        </svg>
      </button>
    </form>
  );
}
