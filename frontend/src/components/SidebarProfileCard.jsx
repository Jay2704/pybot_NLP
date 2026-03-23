import "./SidebarProfileCard.css";

export default function SidebarProfileCard() {
  return (
    <section className="sidebar-profile" aria-label="Profile">
      <div className="sidebar-profile__avatar" aria-hidden>
        AP
      </div>
      <h2 className="sidebar-profile__name">Alex Pythonist</h2>
      <p className="sidebar-profile__role">Senior Developer</p>
      <div className="sidebar-profile__credits">
        <div className="sidebar-profile__credits-row">
          <span className="sidebar-profile__credits-label">Credits</span>
          <span className="sidebar-profile__credits-value">720 / 1,000</span>
        </div>
        <div className="sidebar-profile__bar" role="progressbar" aria-valuenow={72} aria-valuemin={0} aria-valuemax={100}>
          <div className="sidebar-profile__bar-fill" style={{ width: "72%" }} />
        </div>
      </div>
    </section>
  );
}
