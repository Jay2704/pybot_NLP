import { Outlet } from "react-router-dom";
import Navbar from "../Navbar.jsx";
import "./AppShell.css";

export default function AppShell() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="app-shell__main" id="main-content">
        <Outlet />
      </main>
    </div>
  );
}
