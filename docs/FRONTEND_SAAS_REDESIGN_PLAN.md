# Frontend redesign plan — premium SaaS / AI product (React + Vite)

**Scope:** UI/UX and frontend structure only. **No backend, API, or chatbot logic changes.** Same chat request/response contract and response parsing in `api.js`.

**Stack:** React 18, Vite 5, CSS (recommend **CSS variables + modules** or a single `tokens.css` + component-scoped classes). Add **React Router** for multi-page navigation.

---

## 1. Design system (tokens)

Centralize in `frontend/src/styles/tokens.css` (imported once in `main.jsx`).

| Token | Suggestion | Notes |
|--------|----------------|-------|
| **Page background** | `#f4f5f7` or `#f1f3f6` | Light gray, full viewport |
| **Surface / card** | `#ffffff` | White cards |
| **Border** | `1px solid rgba(15, 23, 42, 0.08)` | Soft |
| **Shadow (card)** | `0 1px 3px rgba(15,23,42,0.06), 0 8px 24px rgba(15,23,42,0.06)` | Subtle elevation |
| **Shadow (hover)** | Slightly stronger | Cards / buttons |
| **Primary** | `#6366f1` (indigo-500) | Buttons, links, focus ring |
| **Primary hover** | `#4f46e5` | |
| **Primary subtle** | `rgba(99, 102, 241, 0.1)` | Badges, selected nav |
| **Text primary** | `#0f172a` (slate-900) | Headings |
| **Text secondary** | `#64748b` (slate-500) | Body secondary |
| **Radius** | `12px` cards, `10px` inputs, `9999px` pills | Consistent rounding |
| **Spacing scale** | `4, 8, 12, 16, 24, 32, 48, 64` px | Use as `--space-1` … `--space-8` |
| **Container max-width** | `1120px` or `1200px` | Marketing sections; chat can be `720px` inner column |
| **Typography** | `system-ui, "Inter", …` or Google **Inter** | Bold H1/H2 (600–700), body 400–500 |

**Hierarchy:** Display / H1 → H2 → H3 → body → small / caption (line-height 1.5–1.6).

---

## 2. Reusable components (library)

| Component | Responsibility |
|-----------|----------------|
| `Layout` | Shell: `TopNav` + `<Outlet />` + optional footer |
| `TopNav` | Logo, links (Home, Chatbot, Features, Docs, Tech Stack), Login / Sign Up CTAs; sticky optional; mobile hamburger |
| `Button` | Variants: `primary`, `secondary`, `ghost`, `danger` (optional); sizes `sm` / `md` / `lg` |
| `Card` | Variants: `default`, `elevated`, `outline`; optional `CardHeader`, `CardBody` |
| `Section` | Vertical padding + max-width container + optional title/subtitle |
| `PageHeader` | Title + description for inner pages |
| `Input` / `Label` | For Login/Sign Up forms (even if demo-only) |

Place under `frontend/src/components/ui/` (primitives) vs `frontend/src/components/layout/`.

---

## 3. Routing structure

Install: `react-router-dom`.

```text
/                 → Home (landing)
/chat             → Chatbot (existing chat UI, wrapped in layout)
/features         → Features
/docs             → Docs (static in-app documentation)
/tech-stack       → Tech Stack
/login            → Login (UI only; can be static demo)
/signup           → Sign Up (UI only)
```

**Chat API:** Keep `frontend/src/services/api.js` as-is; `ChatWindow` only mounted on `/chat` (or embedded on Home as optional CTA section — prefer dedicated `/chat` for clarity).

---

## 4. Page-by-page outline

### Home (`/`)
- Hero: headline + subcopy + primary CTA “Open chatbot” → `/chat`, secondary “View features” → `/features`
- 3-column feature strip (icons + short bullets) — teaser, links to `/features`
- Social proof strip (optional): “Stack Overflow data · TF-IDF · FastAPI”
- Footer: minimal links + GitHub

### Chatbot (`/chat`)
- Narrow centered column (`max-width ~720px`) inside a **white `Card`** on gray page background
- Reuse existing bubbles/input; apply design tokens (purple send button, soft borders)
- Optional: compact **page title** “Chat” + one-line product subtitle

### Features (`/`)
- `Section` blocks: retrieval, API, UI, deployment (recruiter bullets)
- Alternating text + placeholder visuals (simple CSS illustrations)

### Docs (`/docs`)
- Static markdown-style sections OR bullet list
- High-level architecture and deployment notes only (no HTTP path reference in copy)

### Tech Stack (`/tech-stack`)
- Grid of tech chips/cards: React, Vite, FastAPI, scikit-learn, pandas, Docker, HF, etc.

### Login / Sign Up (`/login`, `/signup`)
- Centered **Card** with form fields (email/password), primary button
- Disclaimer: “Demo UI — no authentication wired” if not implementing auth (recruiter-transparent)

---

## 5. Responsive behavior

- **Nav:** Horizontal links collapse to hamburger `<768px`
- **Containers:** Horizontal padding `16px` mobile, `24px` tablet+
- **Chat:** Full width on mobile with safe padding; max-width on desktop
- **Typography:** Slightly smaller H1 on mobile

---

## 6. File structure (target)

```text
frontend/src/
  main.jsx
  App.jsx                 # <BrowserRouter> + routes
  styles/
    tokens.css
    global.css            # reset + base body
  components/
    layout/
      Layout.jsx
      TopNav.jsx
      TopNav.css
    ui/
      Button.jsx
      Card.jsx
      Section.jsx
    chat/                 # existing ChatWindow, MessageBubble, SampleQuestions — restyle imports
  pages/
    Home.jsx
    ChatbotPage.jsx       # wraps ChatWindow
    Features.jsx
    DocsPage.jsx
    TechStack.jsx
    Login.jsx
    Signup.jsx
  services/
    api.js                # unchanged
```

---

## 7. Implementation phases (realistic)

| Phase | Work |
|-------|------|
| **1** | Add `react-router-dom`, `tokens.css`, `global.css`, `Layout` + `TopNav` shell |
| **2** | Build `Button`, `Card`, `Section`; migrate **Chat** page + restyle existing chat components |
| **3** | Implement **Home**, **Features**, **Tech Stack** with placeholder content |
| **4** | **Docs** page + **Login/Sign Up** static forms |
| **5** | Responsive nav, a11y pass (focus, landmarks), visual polish |

---

## 8. Constraints (rechecked)

- **API:** Keep existing `api.js` request/response handling unchanged
- **No env changes required** for same-origin HF; dev proxy in `vite.config.js` unchanged
- **Backend:** untouched

This plan is ready to hand to implementation as a sprint backlog; adjust copy and section order per portfolio preference.
