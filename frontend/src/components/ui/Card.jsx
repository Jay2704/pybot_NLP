import "./Card.css";

export default function Card({ as: Comp = "div", variant = "default", className = "", children, ...rest }) {
  const classes = ["ui-card", `ui-card--${variant}`, className].filter(Boolean).join(" ");
  return (
    <Comp className={classes} {...rest}>
      {children}
    </Comp>
  );
}
