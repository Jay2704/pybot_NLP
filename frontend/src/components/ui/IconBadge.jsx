import "./IconBadge.css";

export default function IconBadge({ size = "md", className = "", children, ...rest }) {
  const classes = ["ui-icon-badge", `ui-icon-badge--${size}`, className].filter(Boolean).join(" ");
  return (
    <div className={classes} {...rest}>
      {children}
    </div>
  );
}
