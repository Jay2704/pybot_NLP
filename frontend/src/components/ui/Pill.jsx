import "./Pill.css";

export default function Pill({
  as: Comp = "span",
  variant = "indigo",
  className = "",
  children,
  ...rest
}) {
  const classes = ["ui-pill", `ui-pill--${variant}`, className].filter(Boolean).join(" ");
  return (
    <Comp className={classes} {...rest}>
      {children}
    </Comp>
  );
}
