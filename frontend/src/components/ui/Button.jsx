import "./Button.css";

/**
 * Polymorphic button / link — variants match existing PyBot styles.
 */
export default function Button({
  as: Comp = "button",
  variant = "primary",
  size = "md",
  fullWidth = false,
  className = "",
  children,
  ...rest
}) {
  const classes = ["ui-btn", `ui-btn--${variant}`, `ui-btn--size-${size}`, fullWidth ? "ui-btn--block" : "", className]
    .filter(Boolean)
    .join(" ");
  return (
    <Comp className={classes} {...rest}>
      {children}
    </Comp>
  );
}
