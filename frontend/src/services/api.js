/**
 * FastAPI chat client (JSON chat request with a message field).
 * Response fields used by the UI include answer text and retrieval metadata.
 *
 * Base URL resolution (no chatbot logic here):
 * - If VITE_API_URL is set → use it (cross-origin: separate frontend + API).
 * - Otherwise → "" (relative URLs: same origin as the page — Hugging Face Space, Docker, etc.).
 *
 * Local dev: leave VITE_API_URL unset and run `npm run dev` with Vite proxying API routes to
 * FastAPI (see vite.config.js), or set VITE_API_URL if you prefer direct calls + CORS.
 */

function getApiBase() {
  const raw = import.meta.env.VITE_API_URL;
  if (typeof raw === "string" && raw.trim()) {
    return raw.replace(/\/$/, "");
  }
  return "";
}

const API_BASE = getApiBase();
const CHAT_URL = `${API_BASE}/chat`;

/** Thrown for client validation, HTTP errors, network failures, or malformed responses. */
export class ChatApiError extends Error {
  /**
   * @param {string} message
   * @param {{ status?: number, cause?: unknown }} [opts]
   */
  constructor(message, opts = {}) {
    super(message);
    this.name = "ChatApiError";
    this.status = opts.status;
    this.cause = opts.cause;
  }
}

/**
 * @param {unknown} json
 * @returns {string}
 */
function detailFromFastApiError(json) {
  if (!json || typeof json !== "object") return "";
  const d = /** @type {{ detail?: unknown }} */ (json).detail;
  if (typeof d === "string") return d;
  if (Array.isArray(d)) {
    return d
      .map((item) => {
        if (item && typeof item === "object" && "msg" in item) {
          return String(/** @type {{ msg?: string }} */ (item).msg ?? "");
        }
        return String(item);
      })
      .filter(Boolean)
      .join(" ");
  }
  return "";
}

/**
 * Ensures JSON matches expected ChatResponse shape (display needs `answer`).
 * @param {unknown} data
 * @returns {{ answer: string, alternate: number, qid: number, aid: number }}
 */
function parseChatResponse(data) {
  if (!data || typeof data !== "object") {
    throw new ChatApiError("Invalid response: expected a JSON object");
  }

  const o = /** @type {Record<string, unknown>} */ (data);

  if (typeof o.answer !== "string") {
    throw new ChatApiError("Invalid response: missing or invalid `answer`");
  }

  const qid = o.qid;
  const aid = o.aid;
  const alt = o.alternate;

  if (typeof qid !== "number" || !Number.isFinite(qid)) {
    throw new ChatApiError("Invalid response: missing or invalid `qid`");
  }
  if (typeof aid !== "number" || !Number.isFinite(aid)) {
    throw new ChatApiError("Invalid response: missing or invalid `aid`");
  }
  if (typeof alt !== "number" || !Number.isFinite(alt)) {
    throw new ChatApiError("Invalid response: missing or invalid `alternate`");
  }

  return {
    answer: o.answer,
    alternate: alt,
    qid: Math.trunc(qid),
    aid: Math.trunc(aid),
  };
}

/**
 * @param {string} message
 * @returns {Promise<{ answer: string, alternate: number, qid: number, aid: number }>}
 */
export async function sendChatMessage(message) {
  const text = typeof message === "string" ? message.trim() : "";
  if (!text) {
    throw new ChatApiError("Message cannot be empty");
  }

  let res;
  try {
    res = await fetch(CHAT_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ message: text }),
    });
  } catch (err) {
    const hint =
      API_BASE === ""
        ? "same-origin API (is the backend running, or Vite dev proxy configured?)"
        : `API at ${API_BASE}`;
    const msg =
      err instanceof TypeError && err.message === "Failed to fetch"
        ? `Could not reach the ${hint}`
        : err instanceof Error
          ? `Network error: ${err.message}`
          : "Network error";
    throw new ChatApiError(msg, { cause: err });
  }

  const raw = await res.text();
  const ct = res.headers.get("content-type") || "";

  if (!res.ok) {
    let detail = res.statusText || `HTTP ${res.status}`;
    if (ct.includes("application/json") && raw) {
      try {
        const j = JSON.parse(raw);
        const d = detailFromFastApiError(j);
        if (d) detail = d;
      } catch {
        /* keep statusText */
      }
    }
    throw new ChatApiError(detail || "Request failed", { status: res.status });
  }

  if (!ct.includes("application/json")) {
    throw new ChatApiError("Invalid response: expected application/json");
  }

  let parsed;
  try {
    parsed = raw ? JSON.parse(raw) : null;
  } catch {
    throw new ChatApiError("Invalid response: body is not valid JSON");
  }

  return parseChatResponse(parsed);
}
