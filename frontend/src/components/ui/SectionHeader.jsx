import "./SectionHeader.css";

export default function SectionHeader({
  eyebrow,
  title,
  subtitle,
  align = "left",
  size = "lg",
  highlight,
  titleAs: TitleTag = "h2",
  className = "",
}) {
  const rootClass = ["ui-section-header", `ui-section-header--${align}`, `ui-section-header--${size}`, className]
    .filter(Boolean)
    .join(" ");

  const titleContent =
    title != null && typeof title === "string" && highlight ? (
      <>
        {title}{" "}
        <span className="ui-section-header__highlight">{highlight}</span>
      </>
    ) : (
      title
    );

  return (
    <header className={rootClass}>
      {eyebrow && <p className="ui-section-header__eyebrow">{eyebrow}</p>}
      {title != null && <TitleTag className="ui-section-header__title">{titleContent}</TitleTag>}
      {subtitle && <p className="ui-section-header__subtitle">{subtitle}</p>}
    </header>
  );
}
