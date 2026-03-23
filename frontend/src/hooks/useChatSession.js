import { useState, useCallback, useRef, useEffect } from "react";
import { sendChatMessage, ChatApiError } from "../services/api.js";

function createId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

/**
 * Shared chat state + API calls (same behavior as legacy ChatWindow).
 */
export function useChatSession() {
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

  const appendUser = useCallback((text) => {
    setMessages((prev) => [
      ...prev,
      { id: createId(), role: "user", text, at: Date.now() },
    ]);
  }, []);

  const appendBot = useCallback((text, meta) => {
    setMessages((prev) => [
      ...prev,
      { id: createId(), role: "bot", text, meta, at: Date.now() },
    ]);
  }, []);

  const runSend = useCallback(
    async (rawText) => {
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
    },
    [loading, appendUser, appendBot]
  );

  const handleSubmit = useCallback(
    (e) => {
      e.preventDefault();
      runSend(input);
    },
    [input, runSend]
  );

  const handleClear = useCallback(() => {
    setMessages([]);
    setError(null);
    setInput("");
  }, []);

  return {
    messages,
    input,
    setInput,
    loading,
    error,
    runSend,
    handleSubmit,
    handleClear,
    bottomRef,
  };
}
