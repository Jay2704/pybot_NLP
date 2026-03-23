import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AppShell from "./components/layout/AppShell.jsx";
import Home from "./pages/Home.jsx";
import Chatbot from "./pages/Chatbot.jsx";
import Features from "./pages/Features.jsx";
import Docs from "./pages/Docs.jsx";
import Login from "./pages/Login.jsx";
import Signup from "./pages/Signup.jsx";
import About from "./pages/About.jsx";

/** Matches Vite `base` / `import.meta.env.BASE_URL` (e.g. `/` or `/repo/`). */
function routerBasename() {
  const b = import.meta.env.BASE_URL.replace(/\/$/, "");
  return b === "" ? undefined : b;
}

export default function App() {
  return (
    <BrowserRouter basename={routerBasename()}>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chatbot />} />
          <Route path="/features" element={<Features />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
