import { useChatSession } from "../hooks/useChatSession.js";
import MessageBubble from "../components/MessageBubble.jsx";
import SidebarProfileCard from "../components/SidebarProfileCard.jsx";
import StatsCard from "../components/StatsCard.jsx";
import TopicsCard from "../components/TopicsCard.jsx";
import PromptCard from "../components/PromptCard.jsx";
import ChatInputBar from "../components/ChatInputBar.jsx";
import { Pill } from "../components/ui/index.js";
import "./Chatbot.css";

const PROMPT_QUESTIONS = [
  "What is list comprehension?",
  "How to read a file?",
  "Difference between list and tuple?",
  "What is a lambda function?",
];

const SUGGESTION_CHIPS = [
  "Debugging tracebacks",
  "Virtual environments",
  "Generators & iterators",
  "Error handling",
];

export default function Chatbot() {
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

  const totalQueries = messages.filter((m) => m.role === "user").length;
  const showWelcome = messages.length === 0 && !loading;

  return (
    <div className="chat-dashboard">
      <aside className="chat-dashboard__sidebar">
        <SidebarProfileCard />
        <StatsCard totalQueries={totalQueries} avgResponseLabel="~1.2s" />
        <TopicsCard />
      </aside>

      <div className="chat-dashboard__main">
        <div className="chat-panel">
          <header className="chat-panel__header">
            <div className="chat-panel__title-row">
              <h1 className="chat-panel__title">PyBot v2.4</h1>
              <span className="chat-panel__online">
                <span className="chat-panel__online-dot" aria-hidden />
                Online
              </span>
            </div>
            <div className="chat-panel__toolbar">
              <button
                type="button"
                className="chat-panel__tool-btn"
                aria-label="Search"
                onClick={(e) => e.preventDefault()}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden>
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
              </button>
              <button
                type="button"
                className="chat-panel__tool-btn"
                aria-label="Settings"
                onClick={(e) => e.preventDefault()}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden>
                  <circle cx="12" cy="12" r="3" />
                  <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
                </svg>
              </button>
              <button
                type="button"
                className="chat-panel__tool-btn"
                aria-label="Clear conversation"
                onClick={handleClear}
                title="Clear chat"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden>
                  <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                </svg>
              </button>
            </div>
          </header>

          <div className="chat-panel__scroll">
            {showWelcome ? (
              <div className="chat-panel__welcome">
                <h2>Hello, I&apos;m PyBot</h2>
                <p>
                  How can I help you with Python today? Ask about syntax, libraries, debugging, or
                  best practices—I retrieve answers from Stack Overflow–style knowledge.
                </p>
                <div className="chat-panel__prompts">
                  {PROMPT_QUESTIONS.map((q) => (
                    <PromptCard key={q} disabled={loading} onClick={() => runSend(q)}>
                      {q}
                    </PromptCard>
                  ))}
                </div>
              </div>
            ) : (
              <div className="chat-panel__conversation">
                <div className="chat-panel__messages">
                  {messages.map((m) => (
                    <MessageBubble
                      key={m.id}
                      role={m.role}
                      text={m.text}
                      meta={m.meta}
                      at={m.at}
                      variant="dashboard"
                    />
                  ))}
                  {loading && (
                    <div className="chat-panel__typing" aria-live="polite">
                      <div className="chat-panel__typing-avatar" aria-hidden>
                        AI
                      </div>
                      <div className="chat-panel__typing-bubble">
                        <span className="chat-panel__spinner" aria-hidden />
                        <span className="chat-panel__typing-text">Thinking…</span>
                      </div>
                    </div>
                  )}
                  <div ref={bottomRef} className="chat-panel__scroll-anchor" />
                </div>
              </div>
            )}
          </div>

          {error && <p className="chat-panel__error">{error}</p>}

          {!showWelcome && (
            <div className="chat-panel__chips">
              {SUGGESTION_CHIPS.map((c) => (
                <Pill key={c} as="button" type="button" variant="suggestion" disabled={loading} onClick={() => runSend(c)}>
                  {c}
                </Pill>
              ))}
            </div>
          )}

          <div className="chat-panel__composer">
            <ChatInputBar
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onSubmit={handleSubmit}
              loading={loading}
              disabled={loading}
            />
            <footer className="chat-panel__footer">
              PyBot can make mistakes. Verify important information.
            </footer>
          </div>
        </div>
      </div>
    </div>
  );
}
