import MessageBubble from "./MessageBubble.jsx";
import SampleQuestions from "./SampleQuestions.jsx";
import { useChatSession } from "../hooks/useChatSession.js";
import "./ChatWindow.css";

export default function ChatWindow() {
  const {
    messages,
    input,
    setInput,
    loading,
    error,
    runSend,
    handleSubmit,
    handleClear,
    bottomRef,
  } = useChatSession();

  return (
    <div className="chat-window">
      <header className="chat-window__header">
        <div>
          <h1 className="chat-window__title">PyBot</h1>
          <p className="chat-window__subtitle">Python Q&A — powered by your FastAPI backend</p>
        </div>
        <button type="button" className="chat-window__clear" onClick={handleClear}>
          Clear chat
        </button>
      </header>

      <div className="chat-window__body">
        {messages.length === 0 && !loading && (
          <p className="chat-window__empty">Ask a Python question below, or pick a sample.</p>
        )}
        <div className="chat-window__messages">
          {messages.map((m) => (
            <MessageBubble
              key={m.id}
              role={m.role}
              text={m.text}
              meta={m.meta}
            />
          ))}
          {loading && (
            <div className="chat-window__loading" aria-live="polite">
              <span className="chat-window__spinner" aria-hidden />
              Thinking…
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>

      {error && <p className="chat-window__error">{error}</p>}

      <SampleQuestions onSelect={(q) => runSend(q)} disabled={loading} />

      <form className="chat-window__form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-window__input"
          placeholder="Type your Python question…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          autoComplete="off"
          aria-label="Message"
        />
        <button type="submit" className="chat-window__send" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
