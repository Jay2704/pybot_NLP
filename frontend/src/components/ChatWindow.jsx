import { useState, useCallback, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble.jsx";
import SampleQuestions from "./SampleQuestions.jsx";
import { sendChatMessage, ChatApiError } from "../services/api.js";
import "./ChatWindow.css";

function createId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading, scrollToBottom]);

  const appendUser = (text) => {
    setMessages((prev) => [...prev, { id: createId(), role: "user", text }]);
  };

  const appendBot = (text, meta) => {
    setMessages((prev) => [...prev, { id: createId(), role: "bot", text, meta }]);
  };

  const runSend = async (rawText) => {
    const text = rawText.trim();
    if (!text || loading) return;

    setError(null);
    appendUser(text);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(text);
      appendBot(data.answer, {
        qid: data.qid,
        aid: data.aid,
        alternate: data.alternate,
      });
    } catch (e) {
      const msg =
        e instanceof ChatApiError
          ? e.message
          : e instanceof Error
            ? e.message
            : "Something went wrong";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    runSend(input);
  };

  const handleClear = () => {
    setMessages([]);
    setError(null);
    setInput("");
  };

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
