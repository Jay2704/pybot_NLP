import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppShell from "./components/layout/AppShell.jsx";
import Home from "./pages/Home.jsx";
import Chatbot from "./pages/Chatbot.jsx";
import Features from "./pages/Features.jsx";
import Docs from "./pages/Docs.jsx";
import Login from "./pages/Login.jsx";
import Signup from "./pages/Signup.jsx";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chatbot />} />
          <Route path="/features" element={<Features />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
