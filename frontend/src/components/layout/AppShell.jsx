import { Outlet } from "react-router-dom";
import Navbar from "../Navbar.jsx";
import { PORTFOLIO_URL } from "../../constants/branding.js";
import "./AppShell.css";

export default function AppShell() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="app-shell__main" id="main-content">
        <Outlet />
      </main>
      <footer className="app-shell__footer">
        <p className="app-shell__footer-line">
          Built by Jay
          <span className="app-shell__footer-dot" aria-hidden>
            {" "}
            •{" "}
          </span>
          <a
            href={PORTFOLIO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="app-shell__footer-link"
          >
            View Portfolio
          </a>
        </p>
      </footer>
    </div>
  );
}
