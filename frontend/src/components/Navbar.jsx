import { NavLink, Link } from "react-router-dom";
import { Button } from "./ui/index.js";
import "./Navbar.css";

const navClass = ({ isActive }) =>
  `navbar__link${isActive ? " navbar__link--active" : ""}`;

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar__inner">
        <Link to="/" className="navbar__brand">
          PyBot AI
        </Link>

        <nav className="navbar__links" aria-label="Main">
          <NavLink to="/" end className={navClass}>
            Home
          </NavLink>
          <NavLink to="/chat" className={navClass}>
            Chatbot
          </NavLink>
          <NavLink to="/features" className={navClass}>
            Features
          </NavLink>
          <NavLink to="/docs" className={navClass}>
            Docs
          </NavLink>
          <NavLink to="/about" className={navClass}>
            About
          </NavLink>
        </nav>

        <div className="navbar__cta">
          <Button as={Link} to="/login" variant="ghost">
            Log in
          </Button>
          <Button as={Link} to="/signup" variant="nav-cta">
            Sign Up
          </Button>
        </div>
      </div>
    </header>
  );
}
