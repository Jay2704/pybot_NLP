import { Button } from "./ui/index.js";
import ProfileAvatar from "./ProfileAvatar.jsx";
import { PORTFOLIO_URL } from "../constants/branding.js";
import "./SidebarProfileCard.css";

export default function SidebarProfileCard() {
  return (
    <section className="sidebar-profile" aria-label="Developed by">
      <p className="sidebar-profile__eyebrow">Developed by</p>
      <div className="sidebar-profile__avatar-wrap">
        <ProfileAvatar size="sm" alt="Jay — developer portrait" />
      </div>
      <h2 className="sidebar-profile__name">Jay</h2>
      <p className="sidebar-profile__role">Software Engineer | AI Developer</p>
      <p className="sidebar-profile__tagline">Built PyBot AI</p>
      <Button
        as="a"
        href={PORTFOLIO_URL}
        target="_blank"
        rel="noopener noreferrer"
        variant="secondary"
        size="sm"
        fullWidth
        className="sidebar-profile__cta"
      >
        View Portfolio
      </Button>
    </section>
  );
}
